"""Exercise auto_import.sql on a disposable SQL Server database, never DT05_Dev."""

import os
from pathlib import Path
import sys
import uuid

from dotenv import load_dotenv
import pyodbc

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")


def main():
    from scripts.setup_database import odbc_value

    name = "test_DT05_SqlImport_" + uuid.uuid4().hex[:12]
    os.environ["DT05_SQL_DATABASE"] = name
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django
    django.setup()
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor
    from io import StringIO
    from lichca.models import Branch, Evidence, SwapRequest
    from lichca.demo_dataset import table_counts

    db = settings.DATABASES["default"]
    parts = {"DRIVER": db["OPTIONS"]["driver"], "SERVER": db["HOST"], "DATABASE": "master",
             "Encrypt": os.getenv("DT05_SQL_ENCRYPT", "yes"),
             "TrustServerCertificate": os.getenv("DT05_SQL_TRUST_CERTIFICATE", "yes")}
    if db["USER"]:
        parts.update(UID=db["USER"], PWD=db["PASSWORD"])
    else:
        parts["Trusted_Connection"] = "yes"
    raw = pyodbc.connect(";".join(f"{k}={odbc_value(v)}" for k, v in parts.items()), autocommit=True, timeout=5)
    raw.timeout = 120
    sql = (ROOT / "scripts" / "auto_import.sql").read_text(encoding="utf-8-sig")
    marker = "DECLARE @Database sysname=N'DT05_Demo';"
    assert sql.count(marker) == 1, "Cannot identify SQL database parameter safely."
    sql = sql.replace(marker, f"DECLARE @Database sysname=N'{name}';", 1)

    def execute():
        cursor = raw.cursor()
        try:
            cursor.execute(sql)
            while cursor.nextset():
                pass
        finally:
            cursor.close()

    try:
        execute()
        call_command("check_demo_data", stdout=StringIO())
        initial = table_counts(full=True)
        print("PASS fresh database: SQL schema + full dataset + Django checker")
        assert not MigrationExecutor(connection).migration_plan(MigrationExecutor(connection).loader.graph.leaf_nodes())
        print("PASS Django migration history matches SQL schema")
        execute()
        assert table_counts(full=True) == initial
        print("PASS second run: no duplicate records")
        Branch.objects.create(code="LOCAL_KEEP", name="Local unrelated record")
        missing = Evidence.objects.get(reference="NV10-DAO_TAO_PCCC")
        missing.delete()
        execute()
        assert Evidence.objects.filter(reference="NV10-DAO_TAO_PCCC").count() == 1
        assert Branch.objects.filter(code="LOCAL_KEEP").exists()
        print("PASS repair missing mock row and preserve unrelated data")
        missing = Evidence.objects.get(reference="NV10-DAO_TAO_PCCC")
        missing.delete()
        swap = SwapRequest.objects.order_by("created_at").last()
        original_reason = swap.reason
        swap.reason = "Intentional conflict for rollback test"
        swap.save(update_fields=["reason"])
        try:
            execute()
        except pyodbc.Error as error:
            assert "differs" in str(error) or "differ" in str(error), str(error)
        else:
            raise AssertionError("SQL import should reject modified mock data.")
        assert not Evidence.objects.filter(reference="NV10-DAO_TAO_PCCC").exists()
        assert SwapRequest.objects.get(pk=swap.pk).reason == swap.reason
        print("PASS late conflict: all earlier inserts rolled back")
        swap.reason = original_reason
        swap.save(update_fields=["reason"])
        execute()
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE [lichca_shift] NOCHECK CONSTRAINT [ck_shift_capacity]")
        try:
            execute()
        except pyodbc.Error as error:
            assert "untrusted" in str(error), str(error)
        else:
            raise AssertionError("Disabled constraints should fail readiness.")
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE [lichca_shift] WITH CHECK CHECK CONSTRAINT [ck_shift_capacity]")
        call_command("check_demo_data", stdout=StringIO())
        print("PASS disabled constraint detected; final dataset verified")
        # Reuse only this disposable database to test the old small dataset upgrade.
        call_command("flush", interactive=False, verbosity=0)
        # mssql-django flush re-enables constraints without making them trusted.
        # Revalidate the empty test schema before preparing the legacy dataset.
        from lichca.sql_demo import quote
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT OBJECT_SCHEMA_NAME(parent_object_id), OBJECT_NAME(parent_object_id), name
                FROM sys.foreign_keys WHERE is_not_trusted=1 OR is_disabled=1
                UNION ALL
                SELECT OBJECT_SCHEMA_NAME(parent_object_id), OBJECT_NAME(parent_object_id), name
                FROM sys.check_constraints WHERE is_not_trusted=1 OR is_disabled=1
            """)
            constraints = cursor.fetchall()
            for schema, table, constraint in constraints:
                cursor.execute(f"ALTER TABLE {quote(schema)}.{quote(table)} WITH CHECK CHECK CONSTRAINT {quote(constraint)}")
        from django.contrib.auth import get_user_model
        from lichca.models import Employee, ScheduleGate
        ScheduleGate.objects.create(id=1)
        manager = get_user_model().objects.create_superuser(username="local_setup_admin", password=None)
        call_command("seed_demo", manager=manager.username, stdout=StringIO())
        execute()
        call_command("check_demo_data", stdout=StringIO())
        manager.refresh_from_db()
        assert manager.is_superuser
        assert Evidence.objects.get(reference="NV01-GIAY_BEP").verified_by_id == manager.pk
        assert Employee.objects.get(code="NV01").user.username == "demo_nv01"
        print("PASS SQL upgrades basic dataset and preserves original local manager")
    finally:
        connection.close()
        # Only the unique database created by this invocation can be removed.
        assert name.startswith("test_DT05_SqlImport_") and len(name) == 32
        cursor = raw.cursor()
        cursor.execute(f"IF DB_ID(N'{name}') IS NOT NULL BEGIN ALTER DATABASE [{name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE [{name}]; END")
        cursor.close()
        raw.close()
        print(f"Removed disposable database {name}.")


if __name__ == "__main__":
    main()
