from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from lichca.sql_demo import render_import_sql


class Command(BaseCommand):
    help = "Generate a standalone SQL Server installer matching current Django migrations and full mock data."

    def add_arguments(self, parser):
        parser.add_argument("--output", default=str(Path(settings.BASE_DIR) / "scripts" / "auto_import.sql"))

    def handle(self, *args, **options):
        output = Path(options["output"])
        output.write_text(render_import_sql(), encoding="utf-8-sig")
        self.stdout.write(self.style.SUCCESS(f"Generated {output}"))
