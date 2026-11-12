from io import StringIO
from unittest.mock import patch
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import SimpleTestCase, TestCase

from lichca.models import Assignment, Branch, Employee, Evidence, ScheduleGate, Shift, SundayBaseline, SwapRequest
from lichca.demo_dataset import table_counts
from scripts.setup_database import resolve_manager
from scripts.server_startup import prepare_runserver


class ServerStartupTests(SimpleTestCase):
    @patch.dict("os.environ", {"RUN_MAIN": ""})
    @patch("scripts.server_startup.subprocess.run", return_value=SimpleNamespace(returncode=0))
    def test_database_is_prepared_for_both_runserver_modes(self, run):
        prepare_runserver(["manage.py", "runserver"])
        prepare_runserver(["manage.py", "runserver", "127.0.0.1:8010", "--noreload"])
        self.assertEqual(run.call_count, 2)

    @patch.dict("os.environ", {"RUN_MAIN": "true"})
    @patch("scripts.server_startup.subprocess.run")
    def test_autoreloader_child_does_not_prepare_database_again(self, run):
        prepare_runserver(["manage.py", "runserver"])
        run.assert_not_called()

    @patch.dict("os.environ", {"RUN_MAIN": ""})
    @patch("scripts.server_startup.subprocess.run")
    def test_other_commands_and_help_do_not_write_database(self, run):
        for args in (["manage.py"], ["manage.py", "check"], ["manage.py", "migrate"],
                     ["manage.py", "test"], ["manage.py", "runserver", "--help"]):
            prepare_runserver(args)
        run.assert_not_called()

    @patch.dict("os.environ", {"RUN_MAIN": ""})
    @patch("scripts.server_startup.subprocess.run", return_value=SimpleNamespace(returncode=1))
    def test_sql_failure_stops_server_startup(self, run):
        with self.assertRaises(SystemExit) as error:
            prepare_runserver(["manage.py", "runserver"])
        self.assertEqual(error.exception.code, 1)


class AutomaticSeedTests(TestCase):
    def setUp(self):
        self.manager = get_user_model().objects.create_superuser(
            username="seed_test_admin", password=None,
        )

    def seed(self):
        output = StringIO()
        call_command("seed_demo", manager=self.manager.username, stdout=output)
        return output.getvalue()

    def test_seed_twice_does_not_duplicate(self):
        self.seed()
        self.assertEqual(Employee.objects.count(), 5)
        self.assertEqual(Branch.objects.count(), 2)
        self.assertEqual(Shift.objects.count(), 4)
        self.assertEqual(Evidence.objects.count(), 14)
        self.assertEqual(SundayBaseline.objects.count(), 52)
        self.assertIn("Created 0 records", self.seed())

    def test_conflict_rolls_back_new_records(self):
        Branch.objects.create(code="CN02", name="Different local name")
        with self.assertRaisesMessage(CommandError, "differs from the sample"):
            self.seed()
        self.assertFalse(Branch.objects.filter(code="CN01").exists())
        self.assertEqual(Employee.objects.count(), 0)

    def test_selects_only_active_admin(self):
        self.assertEqual(resolve_manager(), self.manager.username)

    def test_explicit_missing_manager_fails(self):
        with self.assertRaisesMessage(CommandError, "not found"):
            resolve_manager("missing")

    @patch("scripts.setup_database.sys.stdin.isatty", return_value=False)
    def test_multiple_admins_require_selection(self, _isatty):
        get_user_model().objects.create_superuser(username="another_admin", password=None)
        with self.assertRaisesMessage(CommandError, "--manager"):
            resolve_manager()

    @patch("scripts.setup_database.sys.stdin.isatty", return_value=True)
    @patch("django.core.management.call_command")
    def test_first_admin_created_in_same_run(self, command, _isatty):
        self.manager.delete()
        command.side_effect = lambda *a, **kw: get_user_model().objects.create_superuser(
            username="new_local_admin", password=None,
        )
        self.assertEqual(resolve_manager(), "new_local_admin")
        command.assert_called_once_with("createsuperuser", interactive=True)


class FullSeedTests(TestCase):
    def seed(self, **kwargs):
        output = StringIO()
        call_command("seed_demo", full=True, stdout=output, **kwargs)
        return output.getvalue()

    def test_full_dataset_counts_and_repeat(self):
        self.seed()
        for table, actual, minimum in table_counts(full=True):
            with self.subTest(table=table):
                self.assertGreaterEqual(actual, minimum)
        self.assertEqual(get_user_model().objects.count(), 15)
        self.assertEqual(ScheduleGate.objects.count(), 1)
        self.assertEqual(SwapRequest.objects.count(), 5)
        self.assertEqual(SundayBaseline.objects.count(), 520)
        self.assertIn("Created 0 records", self.seed())
        call_command("check_demo_data", stdout=StringIO())

    def test_acceptance_examples_are_preserved(self):
        self.seed()
        self.assertEqual(Assignment.objects.filter(shift__code="CA01").count(), 0)
        self.assertEqual(Assignment.objects.get(shift__code="CA03").employee.code, "NV04")
        self.assertEqual(str(Evidence.objects.get(reference="NV02-GIAY_BEP").valid_until), "2026-11-22")
        self.assertFalse(Evidence.objects.filter(employee__code="NV03", evidence_type__code="IFSG_NHAC").exists())
        self.assertEqual(SundayBaseline.objects.filter(employee__code="NV01", worked_elsewhere=False).count(), 15)
        approved = SwapRequest.objects.get(status="APPROVED")
        self.assertEqual(approved.assignment_a.employee, approved.original_b_employee)
        self.assertEqual(approved.assignment_b.employee, approved.original_a_employee)

    def test_basic_dataset_can_upgrade_without_overwriting_passwords(self):
        manager = get_user_model().objects.create_superuser(username="local_admin", password=None)
        call_command("seed_demo", manager=manager.username, stdout=StringIO())
        self.seed()
        account = get_user_model().objects.get(username="demo_nv01")
        self.assertFalse(account.has_usable_password())
        account.set_password("Local-test-passphrase-456!")
        account.save(update_fields=["password"])
        self.assertIn("Created 0 records", self.seed())
        account.refresh_from_db()
        self.assertTrue(account.check_password("Local-test-passphrase-456!"))
        self.assertEqual(Employee.objects.get(code="NV01").user, account)

    def test_checker_detects_missing_row_even_when_table_still_has_five_rows(self):
        self.seed()
        original = Evidence.objects.get(reference="NV01-GIAY_BEP")
        original.reference = "LOCAL-CHANGED-REFERENCE"
        original.save(update_fields=["reference"])
        self.assertGreater(Evidence.objects.count(), 5)
        with self.assertRaisesMessage(CommandError, "missing sample record"):
            call_command("check_demo_data", stdout=StringIO())

    def test_full_seed_repairs_missing_mock_data_before_web_start(self):
        self.seed()
        Evidence.objects.get(reference="NV10-DAO_TAO_PCCC").delete()
        self.assertIn("Created 1 records", self.seed())
        self.assertEqual(Evidence.objects.filter(reference="NV10-DAO_TAO_PCCC").count(), 1)
        call_command("check_demo_data", stdout=StringIO())

    def test_full_conflict_rolls_back_accounts_and_other_inserts(self):
        Branch.objects.create(code="CN03", name="Existing local branch")
        with self.assertRaisesMessage(CommandError, "differs from the sample"):
            self.seed()
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertFalse(Branch.objects.filter(code="CN01").exists())
