"""One fictional dataset shared by ORM seeding, validation and SQL export."""

from dataclasses import dataclass, field
from datetime import date, datetime
import hashlib
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.db import connection

from lichca.models import (
    Assignment, Branch, Employee, EmployeeBranch, Evidence, EvidenceType,
    ManagerBranch, Position, PositionRequirement, ScheduleGate, Shift,
    SundayBaseline, SwapRequest,
)


@dataclass(frozen=True)
class Ref:
    key: str


@dataclass
class SeedRow:
    model: type
    key: str
    lookup: dict
    values: dict
    create_only: dict = field(default_factory=dict)


def sample_code(shift):
    return hashlib.sha256(f"DT05-demo:{shift}".encode()).hexdigest()[:32]


def build_dataset(*, full=False, manager="quanly01"):
    root = Path(settings.BASE_DIR) / "HO_SO_DT05"
    data = json.loads((root / "du_lieu_mau.json").read_text(encoding="utf-8"))
    extra = json.loads((root / "du_lieu_mau_mo_rong.json").read_text(encoding="utf-8")) if full else {}
    rows = []
    user_model = get_user_model()

    def add(model, key, lookup, values, create_only=None):
        rows.append(SeedRow(model, key, lookup, values, create_only or {}))

    def user(name):
        return Ref(f"User:{manager if name == 'quanly01' else name}")

    def timestamp(value):
        result = datetime.fromisoformat(value) if value else None
        if result is not None and result.utcoffset() is None:
            raise CommandError(f"Timestamp needs a UTC offset: {value}")
        return result

    if full:
        usernames = [f"quanly{i:02}" for i in range(1, 6)]
        usernames += [row["user"] for row in data["employees"] + extra["employees"]]
        for name in usernames:
            # A caller-selected local account is referenced, never modified.
            if name == "quanly01" and manager != name:
                continue
            add(user_model, f"User:{name}", {"username": name}, {
                "is_active": True, "is_staff": False, "is_superuser": False,
            }, {
                "password": "!dt05-demo-no-login", "first_name": "", "last_name": "",
                "email": "", "last_login": None,
                "date_joined": timestamp(data["as_of"]),
            })

    for i, code in enumerate(data["branches"], 1):
        add(Branch, f"Branch:{code}", {"code": code}, {"name": f"Chi nhánh mẫu {i}"})
    for row in extra.get("branches", []):
        add(Branch, f"Branch:{row['code']}", {"code": row["code"]}, {"name": row["name"]})
    for code in data["positions"]:
        add(Position, f"Position:{code}", {"code": code}, {"name": "Bếp"})
    for row in extra.get("positions", []):
        add(Position, f"Position:{row['code']}", {"code": row["code"]}, {"name": row["name"]})

    managers = data["managers"] + extra.get("managers", []) if full else data["managers"][:1]
    for row in managers:
        for code in row["branches"]:
            add(ManagerBranch, f"ManagerBranch:{row['user']}:{code}", {
                "user": user(row["user"]), "branch": Ref(f"Branch:{code}"),
            }, {})

    employees = data["employees"] + extra.get("employees", [])
    for row in employees:
        values = {
            "display_name": row["display_name"], "home_branch": Ref(f"Branch:{row['home_branch']}"),
            "started_on": date.fromisoformat(row["started_on"]), "active": row["active"],
        }
        if full:
            values["user"] = user(row["user"])
        add(Employee, f"Employee:{row['code']}", {"code": row["code"]}, values)
        for code in row["branches"]:
            add(EmployeeBranch, f"EmployeeBranch:{row['code']}:{code}", {
                "employee": Ref(f"Employee:{row['code']}"), "branch": Ref(f"Branch:{code}"),
            }, {})
    for row in data["evidence_types"] + extra.get("evidence_types", []):
        add(EvidenceType, f"EvidenceType:{row['code']}", {"code": row["code"]}, {
            "name": row.get("name", row["code"]), "category": row["category"],
            "expiry_required": row["expiry_required"],
        })
    for code, requirements in (data["position_requirements"] | extra.get("position_requirements", {})).items():
        for evidence in requirements:
            add(PositionRequirement, f"PositionRequirement:{code}:{evidence}", {
                "position": Ref(f"Position:{code}"), "evidence_type": Ref(f"EvidenceType:{evidence}"),
            }, {})
    for row in data["evidence"] + extra.get("evidence", []):
        add(Evidence, f"Evidence:{row['reference']}", {"reference": row["reference"]}, {
            "employee": Ref(f"Employee:{row['employee']}"), "evidence_type": Ref(f"EvidenceType:{row['type']}"),
            "issued_on": date.fromisoformat(row["issued_on"]), "valid_from": date.fromisoformat(row["valid_from"]),
            "valid_until": date.fromisoformat(row["valid_until"]) if row["valid_until"] else None,
            "verified_by": user(row["verified_by"]),
        })
    sundays = data["sunday_baseline"][:]
    if full:
        # Complete the same year for every other employee without altering NV01's quota.
        for employee in employees:
            if employee["code"] != "NV01":
                sundays.extend({"employee": employee["code"], "sunday_date": row["sunday_date"],
                                "worked_elsewhere": False} for row in data["sunday_baseline"])
    for row in sundays:
        day = date.fromisoformat(row["sunday_date"])
        if day.weekday() != 6:
            raise CommandError(f"SundayBaseline {row['employee']} {day}: must be a Sunday.")
        add(SundayBaseline, f"SundayBaseline:{row['employee']}:{day}", {
            "employee": Ref(f"Employee:{row['employee']}"), "sunday_date": day,
        }, {"worked_elsewhere": row["worked_elsewhere"]})
    for row in data["shifts"] + extra.get("shifts", []):
        times = {key: timestamp(row[key]) for key in (
            "start_at", "end_at", "break_start", "break_end", "published_at",
        )}
        add(Shift, f"Shift:{row['code']}", {"code": row["code"]}, {
            **times, "branch": Ref(f"Branch:{row['branch']}"), "position": Ref(f"Position:{row['position']}"),
            "required_count": row["required_count"], "status": row["status"],
            "published_by": user(row["published_by"]) if row["published_by"] else None,
        })
    assignments = data["assignments"] + extra.get("assignments", [])
    for row in assignments:
        code = row.get("public_code") or sample_code(row["shift"])
        add(Assignment, f"Assignment:{row['shift']}", {"public_code": code}, {
            "shift": Ref(f"Shift:{row['shift']}"), "employee": Ref(f"Employee:{row['employee']}"),
        })
    for row in extra.get("swap_requests", []):
        add(SwapRequest, f"SwapRequest:{row['code']}", {
            "assignment_a": Ref(f"Assignment:{row['shift_a']}"),
            "assignment_b": Ref(f"Assignment:{row['shift_b']}"),
            "created_by": user(row["created_by"]), "created_at": timestamp(row["created_at"]),
        }, {
            "original_a_employee": Ref(f"Employee:{row['original_a_employee']}"),
            "original_b_employee": Ref(f"Employee:{row['original_b_employee']}"),
            "status": row["status"], "reason": row["reason"],
            "decided_by": user(row["decided_by"]) if row["decided_by"] else None,
            "decided_at": timestamp(row["decided_at"]),
        })
    known = {f"User:{manager}"} if not full or manager != "quanly01" else set()
    for row in rows:
        if row.key in known:
            raise CommandError(f"{row.key}: duplicate sample key.")
        for value in (row.lookup | row.values).values():
            if isinstance(value, Ref) and value.key not in known:
                raise CommandError(f"{row.key}: missing reference {value.key}.")
        known.add(row.key)
    return rows


def lock_schedule():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM lichca_schedulegate WITH (UPDLOCK, HOLDLOCK) WHERE id=1")
        if cursor.fetchone() is None:
            raise CommandError("ScheduleGate(id=1) missing. Run migrate first.")


def default_manager():
    """Preserve the verifier when extending a previously seeded basic database."""
    owners = list(Evidence.objects.filter(reference="NV01-GIAY_BEP").select_related("verified_by")[:2])
    if len(owners) > 1:
        raise CommandError("Evidence:NV01-GIAY_BEP: duplicate import key.")
    return owners[0].verified_by.username if owners else "quanly01"


def sync_dataset(rows, *, manager, write=False, attach_users=False):
    """Check every sample key, not just counts. Failures roll back in the caller."""
    cache = {}
    if manager not in {row.lookup.get("username") for row in rows if row.model == get_user_model()}:
        account = get_user_model().objects.filter(username=manager, is_active=True).first()
        if account is None:
            raise CommandError(f"Active manager '{manager}' not found. Run createsuperuser first.")
        cache[f"User:{manager}"] = account
    created = attached = 0
    for row in rows:
        def resolve(values):
            return {key: cache[value.key] if isinstance(value, Ref) else value for key, value in values.items()}

        lookup, values = resolve(row.lookup), resolve(row.values)
        matches = list(row.model.objects.filter(**lookup)[:2])
        if len(matches) > 1:
            raise CommandError(f"{row.key}: duplicate import key. Import rolled back.")
        record = matches[0] if matches else None
        if record is None:
            if not write:
                raise CommandError(f"{row.key}: missing sample record. Rerun import to add it.")
            record = row.model(**lookup, **values, **row.create_only)
            # References have already been resolved from checked rows. Let SQL
            # Server enforce FK/UNIQUE/CHECK constraints in this transaction;
            # avoid thousands of redundant FK validation round trips for Sundays.
            record.full_clean(
                exclude=[f.name for f in row.model._meta.fields if f.is_relation],
                validate_unique=False, validate_constraints=False,
            )
            record.save()
            # auto_now_add must retain the fixed historical time from the snapshot.
            fixed_times = {name: value for name, value in (lookup | values).items()
                           if getattr(row.model._meta.get_field(name), "auto_now_add", False)}
            if fixed_times:
                row.model.objects.filter(pk=record.pk).update(**fixed_times)
                for name, value in fixed_times.items():
                    setattr(record, name, value)
            created += 1
        else:
            for name, expected in values.items():
                actual = getattr(record, name)
                if actual == expected:
                    continue
                if write and attach_users and row.model == Employee and name == "user" and actual is None:
                    record.user = expected
                    record.full_clean()
                    record.save(update_fields=["user"])
                    attached += 1
                    continue
                raise CommandError(f"{row.key}: {name} differs from the sample. Import rolled back.")
        cache[row.key] = record
    return created, attached


def table_counts(*, full=False):
    models = [Branch, Position, ManagerBranch, Employee, EmployeeBranch, EvidenceType,
              PositionRequirement, Evidence, SundayBaseline, Shift, Assignment, SwapRequest, ScheduleGate]
    counts = []
    for model in models:
        count = model.objects.count()
        minimum = 1 if model == ScheduleGate else (5 if full else 0)
        if count < minimum or (model == ScheduleGate and count != 1):
            raise CommandError(f"{model._meta.db_table}: {count} records; requires {minimum}.")
        counts.append((model._meta.db_table, count, minimum))
    return counts
