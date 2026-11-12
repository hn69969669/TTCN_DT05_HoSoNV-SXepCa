from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from lichca.demo_dataset import build_dataset, default_manager, lock_schedule, sync_dataset, table_counts


class Command(BaseCommand):
    help = "Import fictional DT05 data atomically; --full supplies 5+ rows per business table."

    def add_arguments(self, parser):
        parser.add_argument("--manager", help="Existing local username; full demo defaults to quanly01.")
        parser.add_argument("--full", action="store_true", help="Include accounts, additional branches and swap history.")

    @transaction.atomic
    def handle(self, *args, **options):
        full = options["full"]
        lock_schedule()
        manager = options["manager"] or (default_manager() if full else None)
        if not manager:
            raise CommandError("Basic seed requires --manager with an existing local username.")
        rows = build_dataset(full=full, manager=manager)
        created, attached = sync_dataset(rows, manager=manager, write=True, attach_users=full)
        counts = table_counts(full=full)
        self.stdout.write(self.style.SUCCESS(
            f"Sample import completed. Created {created} records. Attached {attached} employee accounts."
        ))
        for table, count, minimum in counts:
            self.stdout.write(f"  {table}: {count} (minimum {minimum})")
        if full:
            self.stdout.write(f"Primary sample manager: {manager}")
            self.stdout.write("Demo accounts have no login password. Use manage.py changepassword USERNAME to enable login.")
