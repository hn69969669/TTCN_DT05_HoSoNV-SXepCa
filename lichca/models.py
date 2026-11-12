import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


def assignment_code():
    return uuid.uuid4().hex


class Branch(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code} · {self.name}"


class Position(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code} · {self.name}"


class ManagerBranch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "branch"], name="uq_manager_branch"),
        ]


class Employee(models.Model):
    code = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=150)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="employee_profiles",
    )
    home_branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    started_on = models.DateField()
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(user__isnull=False),
                name="uq_employee_user_present",
            ),
        ]

    def __str__(self):
        return f"{self.code} · {self.display_name}"


class EmployeeBranch(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["employee", "branch"], name="uq_employee_branch"),
        ]


class EvidenceType(models.Model):
    class Category(models.TextChoices):
        DOCUMENT = "DOCUMENT", "Giấy tờ"
        TRAINING = "TRAINING", "Đào tạo"

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=10, choices=Category.choices)
    expiry_required = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(category__in=["DOCUMENT", "TRAINING"]),
                name="ck_evidence_category",
            ),
        ]

    def __str__(self):
        return f"{self.code} · {self.name}"


class PositionRequirement(models.Model):
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    evidence_type = models.ForeignKey(EvidenceType, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["position", "evidence_type"], name="uq_position_evidence"
            ),
        ]


class Evidence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    evidence_type = models.ForeignKey(EvidenceType, on_delete=models.PROTECT)
    issued_on = models.DateField()
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=100)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(valid_until__isnull=True) | Q(valid_until__gte=F("valid_from")),
                name="ck_evidence_dates",
            ),
        ]
        indexes = [
            models.Index(
                fields=["employee", "evidence_type", "valid_from"],
                name="ix_evidence_employee_type",
            ),
        ]


class SundayBaseline(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    sunday_date = models.DateField()
    worked_elsewhere = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "sunday_date"], name="uq_employee_sunday"
            ),
        ]


class Shift(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Nháp"
        PUBLISHED = "PUBLISHED", "Đã công bố"

    code = models.CharField(max_length=30, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    break_start = models.DateTimeField(null=True, blank=True)
    break_end = models.DateTimeField(null=True, blank=True)
    required_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(end_at__gt=F("start_at")), name="ck_shift_time"),
            models.CheckConstraint(condition=Q(required_count__gt=0), name="ck_shift_capacity"),
            models.CheckConstraint(
                condition=(
                    Q(break_start__isnull=True, break_end__isnull=True)
                    | Q(
                        break_start__isnull=False,
                        break_end__isnull=False,
                        break_start__gte=F("start_at"),
                        break_end__lte=F("end_at"),
                        break_end__gt=F("break_start"),
                    )
                ),
                name="ck_shift_break",
            ),
            models.CheckConstraint(
                condition=(
                    Q(break_start__isnull=True)
                    | Q(break_start__gt=F("start_at"))
                    | Q(break_end__lt=F("end_at"))
                ),
                name="ck_shift_work_positive",
            ),
            models.CheckConstraint(
                condition=(
                    Q(status="DRAFT", published_at__isnull=True, published_by__isnull=True)
                    | Q(
                        status="PUBLISHED",
                        published_at__isnull=False,
                        published_by__isnull=False,
                    )
                ),
                name="ck_shift_publication",
            ),
        ]
        indexes = [
            models.Index(fields=["branch", "start_at"], name="ix_shift_branch_start"),
        ]

    def __str__(self):
        return self.code


class Assignment(models.Model):
    public_code = models.CharField(max_length=32, unique=True, default=assignment_code)
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["shift", "employee"], name="uq_shift_employee"),
        ]
        indexes = [
            models.Index(fields=["employee", "shift"], name="ix_assignment_employee_shift"),
        ]


class SwapRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Chờ duyệt"
        APPROVED = "APPROVED", "Đã duyệt"
        REJECTED = "REJECTED", "Từ chối"

    assignment_a = models.ForeignKey(
        Assignment, on_delete=models.PROTECT, related_name="swap_offers"
    )
    assignment_b = models.ForeignKey(
        Assignment, on_delete=models.PROTECT, related_name="swap_targets"
    )
    original_a_employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="original_swap_offers"
    )
    original_b_employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="original_swap_targets"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_swaps"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="decided_swaps",
        null=True,
        blank=True,
    )
    decided_at = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(assignment_a=F("assignment_b")), name="ck_swap_two_assignments"
            ),
            models.CheckConstraint(
                condition=~Q(original_a_employee=F("original_b_employee")),
                name="ck_swap_two_employees",
            ),
            models.CheckConstraint(
                condition=(
                    Q(status="PENDING", decided_at__isnull=True, decided_by__isnull=True)
                    | Q(
                        status__in=["APPROVED", "REJECTED"],
                        decided_at__isnull=False,
                        decided_by__isnull=False,
                    )
                ),
                name="ck_swap_decision",
            ),
            models.CheckConstraint(
                condition=~Q(status="REJECTED") | ~Q(reason=""),
                name="ck_swap_rejection_reason",
            ),
        ]
        indexes = [
            models.Index(fields=["status", "created_at"], name="ix_swap_status_created"),
        ]


class ScheduleGate(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(id=1), name="ck_schedule_gate_singleton"),
        ]
