"""Build a standalone SQL Server installer from migrations and the shared mock data."""

from datetime import date, datetime, timezone
import re

from django.apps import apps
from django.core.management.base import CommandError
from django.db import connection
from django.db.migrations import RunPython, RunSQL
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder

from lichca.demo_dataset import Ref, build_dataset
from lichca.models import Employee, ScheduleGate


def quote(value):
    return "[" + value.replace("]", "]]") + "]"


def literal(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, datetime):
        stamp = value.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="microseconds")
        return f"CONVERT(datetime2(6), N'{stamp}', 126)"
    if isinstance(value, date):
        return f"CONVERT(date, N'{value.isoformat()}', 23)"
    return "N'" + str(value).replace("'", "''") + "'"


def migration_plan():
    loader = MigrationLoader(None)
    names = []
    for leaf in sorted(loader.graph.leaf_nodes()):
        for name in loader.graph.forwards_plan(leaf):
            if name not in names:
                names.append(name)
    loader.connection = connection
    return loader, names


def schema_sql(loader, names):
    # Build the final ProjectState rather than replaying historical ALTER SQL:
    # SQL Server generates names for inline UNIQUE constraints, so offline
    # sqlmigrate output can refer to constraint names from the exporting machine.
    for name in names:
        for operation in loader.get_migration(*name).operations:
            handled = {("lichca", "0002_schedule_gate"),
                       ("contenttypes", "0002_remove_content_type_name"),
                       ("auth", "0011_update_proxy_permissions")}
            # Empty databases have no legacy content types/proxy permissions;
            # content_types_sql() creates final metadata, and id=1 is explicit.
            if isinstance(operation, (RunPython, RunSQL)) and name not in handled:
                raise CommandError(f"SQL export needs an explicit equivalent for data migration {name}.")
    state = loader.project_state()
    with connection.schema_editor(collect_sql=True, atomic=False) as editor:
        editor.create_model(MigrationRecorder.Migration)
        for model in state.apps.get_models():
            editor.create_model(model)
    statements = [sql for sql in editor.collected_sql if sql.startswith("CREATE TABLE")]
    statements += sorted(sql for sql in editor.collected_sql if not sql.startswith("CREATE TABLE"))
    statements.append("INSERT INTO [lichca_schedulegate] ([id]) VALUES (1);")
    for app, name in names:
        statements.append(
            "INSERT INTO [django_migrations] ([app], [name], [applied]) VALUES "
            f"({literal(app)}, {literal(name)}, SYSUTCDATETIME());"
        )
    return "\n".join(statements)


def schema_checks(names):
    checks = []
    for app, name in names:
        checks.append(
            f"IF NOT EXISTS (SELECT 1 FROM [django_migrations] WHERE [app]={literal(app)} AND [name]={literal(name)})\n"
            "    THROW 51000, 'Schema version differs. Run the PowerShell importer to migrate first.', 1;"
        )
    expected = " OR ".join(f"([app]={literal(app)} AND [name]={literal(name)})" for app, name in names)
    checks.append(
        f"IF EXISTS (SELECT 1 FROM [django_migrations] WHERE NOT ({expected}))\n"
        "    THROW 51000, 'Database has migrations outside this SQL snapshot. Regenerate the SQL file.', 1;"
    )
    # Include through tables and framework tables; never mark an incomplete schema as ready.
    # Auto-created auth through tables use the historical migration state's
    # default PK type, which can differ from the live AppConfig default.
    schema_models = MigrationLoader(None).project_state().apps.get_models(include_auto_created=True)
    for model in list(schema_models) + [MigrationRecorder.Migration]:
        table = model._meta.db_table
        for field in model._meta.local_fields:
            checks.append(
                f"IF COL_LENGTH({literal(table)}, {literal(field.column)}) IS NULL\n"
                f"    THROW 51000, {literal('Missing schema column: ' + table + '.' + field.column)}, 1;"
            )
            data_type = re.fullmatch(r"(\w+)(?:\((max|\d+)\))?", field.db_type(connection), re.IGNORECASE)
            if data_type:
                type_name, length = data_type.groups()
                conditions = [f"TYPE_NAME(c.system_type_id)={literal(type_name)}", f"c.is_nullable={int(field.null)}"]
                if length is not None:
                    size = -1 if length.lower() == "max" else int(length) * (2 if type_name.lower() in {"nvarchar", "nchar"} else 1)
                    conditions.append(f"c.max_length={size}")
                auto = field.get_internal_type() in {"AutoField", "BigAutoField", "SmallAutoField"}
                conditions.append(f"c.is_identity={int(auto)}")
                checks.append(
                    f"IF NOT EXISTS (SELECT 1 FROM sys.columns c WHERE c.object_id=OBJECT_ID({literal(table)}) "
                    f"AND c.name={literal(field.column)} AND {' AND '.join(conditions)})\n"
                    f"    THROW 51000, {literal('Column type/null/identity differs: ' + table + '.' + field.column)}, 1;"
                )
            if field.is_relation and field.many_to_one and field.db_constraint:
                target = field.target_field
                checks.append(
                    "IF NOT EXISTS (SELECT 1 FROM sys.foreign_key_columns f "
                    "JOIN sys.columns c ON c.object_id=f.parent_object_id AND c.column_id=f.parent_column_id "
                    "JOIN sys.columns r ON r.object_id=f.referenced_object_id AND r.column_id=f.referenced_column_id "
                    f"WHERE f.parent_object_id=OBJECT_ID({literal(table)}) AND c.name={literal(field.column)} "
                    f"AND f.referenced_object_id=OBJECT_ID({literal(target.model._meta.db_table)}) AND r.name={literal(target.column)})\n"
                    f"    THROW 51000, {literal('Missing FK: ' + table + '.' + field.column)}, 1;"
                )
            if field.unique or field.primary_key:
                flag = "is_primary_key" if field.primary_key else "is_unique"
                checks.append(
                    "IF NOT EXISTS (SELECT 1 FROM sys.indexes i "
                    "JOIN sys.index_columns k ON k.object_id=i.object_id AND k.index_id=i.index_id "
                    "JOIN sys.columns c ON c.object_id=k.object_id AND c.column_id=k.column_id "
                    f"WHERE i.object_id=OBJECT_ID({literal(table)}) AND i.{flag}=1 AND c.name={literal(field.column)} "
                    "AND (SELECT COUNT(*) FROM sys.index_columns k2 WHERE k2.object_id=i.object_id AND k2.index_id=i.index_id AND k2.key_ordinal>0)=1)\n"
                    f"    THROW 51000, {literal('Missing unique/primary key: ' + table + '.' + field.column)}, 1;"
                )
        for constraint in model._meta.constraints:
            checks.append(
                f"IF OBJECT_ID({literal(table)}, 'U') IS NULL OR NOT EXISTS ("
                f"SELECT 1 FROM sys.objects WHERE parent_object_id=OBJECT_ID({literal(table)}) AND name={literal(constraint.name)} "
                f"UNION ALL SELECT 1 FROM sys.indexes WHERE object_id=OBJECT_ID({literal(table)}) AND name={literal(constraint.name)})\n"
                f"    THROW 51000, {literal('Missing schema constraint: ' + constraint.name)}, 1;"
            )
        for index in model._meta.indexes:
            checks.append(
                f"IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE object_id=OBJECT_ID({literal(table)}) AND name={literal(index.name)} AND is_disabled=0)\n"
                f"    THROW 51000, {literal('Missing index: ' + index.name)}, 1;"
            )
    checks.append("""IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE is_disabled=1 OR is_not_trusted=1)
    OR EXISTS (SELECT 1 FROM sys.check_constraints WHERE is_disabled=1 OR is_not_trusted=1)
    THROW 51000, 'Disabled or untrusted FK/CHECK constraint. Repair schema before import.', 1;""")
    return "\n".join(checks)


def content_types_sql():
    statements = []
    for model in apps.get_models():
        app, name = model._meta.app_label, model._meta.model_name
        where = f"[app_label]={literal(app)} AND [model]={literal(name)}"
        statements.append(
            f"IF NOT EXISTS (SELECT 1 FROM [django_content_type] WHERE {where})\n"
            f"    INSERT INTO [django_content_type] ([app_label], [model]) VALUES ({literal(app)}, {literal(name)});"
        )
        for action in model._meta.default_permissions:
            code = f"{action}_{name}"
            ct = f"(SELECT [id] FROM [django_content_type] WHERE {where})"
            statements.append(
                f"IF NOT EXISTS (SELECT 1 FROM [auth_permission] WHERE [content_type_id]={ct} AND [codename]={literal(code)})\n"
                f"    INSERT INTO [auth_permission] ([name], [content_type_id], [codename]) VALUES "
                f"({literal('Can ' + action + ' ' + str(model._meta.verbose_name))}, {ct}, {literal(code)});"
            )
    return "\n".join(statements)


def seed_sql():
    rows = build_dataset(full=True)
    variables = {row.key: f"@r{i}" for i, row in enumerate(rows)}
    statements = ["""DECLARE @created int=0, @attached int=0, @seed_owner bigint;
-- Preserve a local manager from an earlier basic import, without changing its privileges.
SELECT @seed_owner=u.[id] FROM [lichca_evidence] e JOIN [auth_user] u ON u.[id]=e.[verified_by_id]
WHERE e.[reference]=N'NV01-GIAY_BEP' AND u.[username]<>N'quanly01';
IF @seed_owner IS NOT NULL AND NOT EXISTS (SELECT 1 FROM [auth_user] WHERE [id]=@seed_owner AND [is_active]=1)
    THROW 51000, 'Existing sample manager is inactive. Choose an active local manager explicitly using PowerShell.', 1;
"""]
    for row in rows:
        table = quote(row.model._meta.db_table)
        variable = variables[row.key]

        def values_sql(values):
            return {quote(row.model._meta.get_field(k).column): variables[v.key] if isinstance(v, Ref) else literal(v)
                    for k, v in values.items()}

        lookup, values, create = values_sql(row.lookup), values_sql(row.values), values_sql(row.create_only)
        where = " AND ".join(f"{k}={v}" for k, v in lookup.items())
        statements.extend([
            f"-- {row.key}", f"DECLARE {variable} bigint;",
        ])
        if row.key == "User:quanly01":
            statements.append("IF @seed_owner IS NULL\nBEGIN")
        statements.extend([
            f"IF (SELECT COUNT_BIG(*) FROM {table} WHERE {where})>1",
            f"    THROW 51000, {literal(row.key + ': duplicate import key. Import rolled back.')}, 1;",
            f"SELECT {variable}=[id] FROM {table} WHERE {where};",
            f"IF {variable} IS NULL\nBEGIN",
        ])
        insert = lookup | values | create
        statements.extend([
            f"    INSERT INTO {table} ({', '.join(insert)}) VALUES ({', '.join(insert.values())});",
            f"    SET {variable}=CONVERT(bigint, SCOPE_IDENTITY());",
            "    SET @created+=1;", "END\nELSE\nBEGIN",
            f"    SET {variable}={variable};",
        ])
        if row.model == Employee:
            statements.extend([
                f"    IF EXISTS (SELECT 1 FROM {table} WHERE [id]={variable} AND [user_id] IS NULL)",
                "    BEGIN",
                f"        UPDATE {table} SET [user_id]={values['[user_id]']} WHERE [id]={variable};",
                "        SET @attached+=1;", "    END;",
            ])
        if values:
            statements.extend([
                f"    IF EXISTS (SELECT {', '.join(values)} FROM {table} WHERE [id]={variable}",
                f"               EXCEPT SELECT {', '.join(values.values())})",
                f"        THROW 51000, {literal(row.key + ': values differ from sample. Import rolled back.')}, 1;",
            ])
        statements.append("END;")
        if row.key == "User:quanly01":
            statements.append(f"END\nELSE SET {variable}=@seed_owner;")
    statements.append(content_types_sql())
    statements.append("DECLARE @counts TABLE ([table_name] nvarchar(128), [actual] bigint, [minimum] int);")
    models = {row.model for row in rows} | {ScheduleGate}
    for model in sorted(models, key=lambda m: m._meta.db_table):
        minimum = 1 if model == ScheduleGate else 5
        table = model._meta.db_table
        statements.append(f"INSERT INTO @counts SELECT {literal(table)}, COUNT_BIG(*), {minimum} FROM {quote(table)};")
    statements.extend([
        "IF EXISTS (SELECT 1 FROM @counts WHERE [actual]<[minimum])",
        "    THROW 51000, 'Insufficient mock rows. Import rolled back.', 1;",
        "IF (SELECT COUNT(*) FROM [lichca_schedulegate])<>1 OR NOT EXISTS (SELECT 1 FROM [lichca_schedulegate] WHERE [id]=1)",
        "    THROW 51000, 'ScheduleGate must have exactly one row id=1.', 1;",
        "SELECT @created AS [created_records], @attached AS [attached_accounts];",
        "SELECT *, N'OK' AS [result] FROM @counts ORDER BY [table_name];",
        "PRINT N'DATA READY: schema and full mock data verified. Accounts need local passwords. Application YC/T checks remain separate.';",
    ])
    return "\n".join(statements)


def render_import_sql():
    loader, names = migration_plan()
    schema = schema_sql(loader, names)
    checks = schema_checks(names)
    seed = seed_sql()
    # Dynamic batches allow fresh schema creation and subsequent reads in one run,
    # without GO continuing after a failed batch. All data writes share the gate.
    body = f"""SET NOCOUNT ON;
SET XACT_ABORT ON;
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
DECLARE @stage nvarchar(50)=N'lock';
BEGIN TRY
    BEGIN TRANSACTION;
    DECLARE @lock_result int;
    EXEC @lock_result=sys.sp_getapplock @Resource=N'DT05-auto-import', @LockMode='Exclusive', @LockOwner='Transaction', @LockTimeout=60000;
    IF @lock_result<0 THROW 51000, 'Cannot lock database setup. Retry after other import finishes.', 1;
    IF OBJECT_ID(N'django_migrations', 'U') IS NULL
    BEGIN
        IF EXISTS (SELECT 1 FROM sys.tables WHERE is_ms_shipped=0)
            THROW 51000, 'Non-empty database without migration history. Choose a new DT05 database.', 1;
        SET @stage=N'schema creation';
        EXEC sys.sp_executesql {literal(schema)};
    END;
    SET @stage=N'schema verification';
    EXEC sys.sp_executesql {literal(checks)};
    EXEC sys.sp_executesql N'
        IF NOT EXISTS (SELECT 1 FROM [lichca_schedulegate] WITH (UPDLOCK, HOLDLOCK) WHERE [id]=1)
            THROW 51000, ''ScheduleGate missing. Repair migration 0002 before import.'', 1;';
    SET @stage=N'mock data';
    EXEC sys.sp_executesql {literal(seed)};
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE()<>0 ROLLBACK TRANSACTION;
    DECLARE @error nvarchar(2048)=CONCAT(@stage, N' line ', ERROR_LINE(), N': ', ERROR_MESSAGE());
    THROW 51000, @error, 1;
END CATCH;
"""
    return f"""-- DT05: standalone SQL Server import (SSMS / sqlcmd / ODBC).
-- Generated by manage.py export_demo_sql. Sources: migrations + both mock JSON files.
-- Edit ONLY @Database below, select this entire file, then Execute (F5).
-- Existing data is preserved; mismatched sample keys abort and roll back this run.
-- 12 business tables have 5+ rows. ScheduleGate is a singleton (exactly id=1).
-- Django sessions/logs/groups are framework tables; no fake login sessions or audit logs.
-- Demo accounts cannot log in until manage.py changepassword USERNAME is run locally.
-- Dates are fixed in Nov/Dec 2026; use simulated as_of=2026-11-20 for acceptance scenarios.
SET NOCOUNT ON;
SET XACT_ABORT ON;
DECLARE @Database sysname=N'DT05_Demo';
IF @Database IS NULL OR LEN(LTRIM(RTRIM(@Database)))=0 OR LOWER(@Database) IN (N'master', N'model', N'msdb', N'tempdb')
    THROW 51000, 'Choose a non-system DT05 database name.', 1;
IF @@TRANCOUNT<>0 THROW 51000, 'Run this installer outside an existing transaction.', 1;
IF DB_ID(@Database) IS NULL
BEGIN
    DECLARE @create_db nvarchar(max)=N'CREATE DATABASE '+QUOTENAME(@Database);
    EXEC sys.sp_executesql @create_db;
END;
DECLARE @install nvarchar(max)=N'USE '+QUOTENAME(@Database)+N';\n'+{literal(body)};
EXEC sys.sp_executesql @install;
"""
