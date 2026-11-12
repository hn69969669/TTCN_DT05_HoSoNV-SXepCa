from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.db.migrations.executor import MigrationExecutor

from lichca.demo_dataset import build_dataset, default_manager, lock_schedule, sync_dataset, table_counts
from lichca.sql_demo import migration_plan, schema_checks


class Command(BaseCommand):
    help = "Read-only verification of schema, constraints and every key in the full DT05 dataset."

    def add_arguments(self, parser):
        parser.add_argument("--manager")

    @transaction.atomic
    def handle(self, *args, **options):
        executor = MigrationExecutor(connection)
        if executor.migration_plan(executor.loader.graph.leaf_nodes()):
            raise CommandError("Unapplied migrations. Run migrate before checking sample data.")
        lock_schedule()
        manager = options["manager"] or default_manager()
        _, names = migration_plan()
        with connection.cursor() as cursor:
            cursor.execute(schema_checks(names))
        sync_dataset(build_dataset(full=True, manager=manager), manager=manager)
        counts = table_counts(full=True)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sys.foreign_keys WHERE is_disabled=1 OR is_not_trusted=1
                UNION ALL
                SELECT name FROM sys.check_constraints WHERE is_disabled=1 OR is_not_trusted=1
            """)
            disabled = [row[0] for row in cursor.fetchall()]
        if disabled:
            raise CommandError(f"Disabled or untrusted constraints: {', '.join(disabled)}")
        for table, count, minimum in counts:
            self.stdout.write(f"OK {table}: {count} / minimum {minimum}")
        self.stdout.write(self.style.SUCCESS("DATA READY: full DT05 mock dataset verified. This does not certify application features."))
