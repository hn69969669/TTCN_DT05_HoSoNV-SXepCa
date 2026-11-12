import json
from datetime import date, datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from lichca.models import (
    Assignment, Branch, Employee, EmployeeBranch, Evidence, EvidenceType,
    ManagerBranch, Position, PositionRequirement, Shift, SundayBaseline,
)


class Command(BaseCommand):
    help = "Import the bundled fictional DT05 dataset without overwriting existing records."

    def add_arguments(self, parser):
        parser.add_argument("--manager", required=True, help="Existing local username.")

    def ensure(self, model, lookup, values):
        matches = list(model.objects.filter(**lookup)[:2])
        if len(matches) > 1:
            raise CommandError(f"{model.__name__} {lookup}: duplicate import key.")
        record = matches[0] if matches else None
        if record:
            for field, expected in values.items():
                actual = getattr(record, field)
                if actual != expected:
                    raise CommandError(
                        f"{model.__name__} {lookup}: {field} differs from the sample. "
                        "Import rolled back."
                    )
            return record
        record = model(**lookup, **values)
        record.full_clean()
        record.save()
        self.created += 1
        return record

    @transaction.atomic
    def handle(self, *args, **options):
        manager = get_user_model().objects.filter(username=options["manager"]).first()
        if manager is None:
            raise CommandError("Manager username not found. Run createsuperuser first.")
        data = json.loads(
            (Path(settings.BASE_DIR) / "HO_SO_DT05" / "du_lieu_mau.json").read_text(encoding="utf-8")
        )
        # All writes affecting schedule validation share the same gate.
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM lichca_schedulegate WITH (UPDLOCK, HOLDLOCK) WHERE id=1")
            if cursor.fetchone() is None:
                raise CommandError("Schedule gate missing. Run migrate first.")
        self.created = 0
        branches = {
            code: self.ensure(Branch, {"code": code}, {"name": f"Chi nhánh mẫu {i}"})
            for i, code in enumerate(data["branches"], 1)
        }
        positions = {
            code: self.ensure(Position, {"code": code}, {"name": "Bếp"})
            for code in data["positions"]
        }
        self.ensure(ManagerBranch, {"user": manager, "branch": branches["CN01"]}, {})
        employees = {}
        for row in data["employees"]:
            employee = self.ensure(Employee, {"code": row["code"]}, {
                "display_name": row["display_name"],
                "home_branch": branches[row["home_branch"]],
                "started_on": date.fromisoformat(row["started_on"]),
                "active": row["active"],
            })
            employees[row["code"]] = employee
            for code in row["branches"]:
                self.ensure(EmployeeBranch, {"employee": employee, "branch": branches[code]}, {})
        types = {}
        for row in data["evidence_types"]:
            types[row["code"]] = self.ensure(EvidenceType, {"code": row["code"]}, {
                "name": row["code"],
                "category": row["category"],
                "expiry_required": row["expiry_required"],
            })
        for position, requirements in data["position_requirements"].items():
            for code in requirements:
                self.ensure(PositionRequirement, {
                    "position": positions[position], "evidence_type": types[code],
                }, {})
        for row in data["evidence"]:
            self.ensure(Evidence, {"reference": row["reference"]}, {
                "employee": employees[row["employee"]],
                "evidence_type": types[row["type"]],
                "issued_on": date.fromisoformat(row["issued_on"]),
                "valid_from": date.fromisoformat(row["valid_from"]),
                "valid_until": date.fromisoformat(row["valid_until"]) if row["valid_until"] else None,
                "verified_by": manager,
            })
        for row in data["sunday_baseline"]:
            day = date.fromisoformat(row["sunday_date"])
            if day.weekday() != 6:
                raise CommandError(f"{day} must be a Sunday.")
            self.ensure(SundayBaseline, {
                "employee": employees[row["employee"]], "sunday_date": day,
            }, {"worked_elsewhere": row["worked_elsewhere"]})
        shifts = {}
        for row in data["shifts"]:
            times = {
                key: datetime.fromisoformat(row[key]) if row[key] else None
                for key in ("start_at", "end_at", "break_start", "break_end", "published_at")
            }
            shifts[row["code"]] = self.ensure(Shift, {"code": row["code"]}, {
                **times,
                "branch": branches[row["branch"]],
                "position": positions[row["position"]],
                "required_count": row["required_count"],
                "status": row["status"],
                "published_by": manager if row["published_by"] else None,
            })
        for row in data["assignments"]:
            self.ensure(Assignment, {"public_code": row["public_code"]}, {
                "shift": shifts[row["shift"]], "employee": employees[row["employee"]],
            })
        self.stdout.write(self.style.SUCCESS(
            f"Sample import completed. Created {self.created} records. "
            "Employees: 5; branches: 2; shifts: 4; evidence: 14; Sundays: 52."
        ))
