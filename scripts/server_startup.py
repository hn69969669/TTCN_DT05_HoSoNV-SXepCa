"""Prepare DT05 SQL data once before a development server starts listening."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def prepare_runserver(argv=None):
    arguments = sys.argv if argv is None else argv
    if len(arguments) < 2 or arguments[1] != "runserver":
        return
    if any(flag in arguments[2:] for flag in ("--help", "-h", "--version")):
        return
    # Django's autoreloader launches a child process and relaunches it on edits.
    # Only the initial parent should migrate/seed, before any HTTP requests.
    if os.environ.get("RUN_MAIN") == "true":
        return

    print("Checking SQL Server, migrations and required demo data before starting the web...", flush=True)
    result = subprocess.run(
        [sys.executable, "-u", str(ROOT / "scripts" / "setup_database.py")],
        cwd=ROOT,
        check=False,
    )
    if result.returncode:
        print("Web startup stopped: database preparation failed. Fix the SQL/data error above and retry.", file=sys.stderr)
        raise SystemExit(result.returncode)
    print("Database ready. Starting Django development server...", flush=True)
