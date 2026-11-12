"""Create the local SQL Server database and apply the project's migrations."""

import argparse
import os
from pathlib import Path
import re
import secrets
import sys

import pyodbc
from dotenv import dotenv_values, load_dotenv, set_key

ROOT = Path(__file__).resolve().parent.parent


def resolve_manager(username=None):
    """Use a local account, or create the first admin interactively."""
    from django.contrib.auth import get_user_model
    from django.core.management import call_command, CommandError

    users = get_user_model().objects
    if username:
        if not users.filter(username=username, is_active=True).exists():
            raise CommandError(f"Active manager '{username}' not found. Run createsuperuser first.")
        return username
    admins = list(users.filter(is_superuser=True, is_active=True).values_list("username", flat=True))
    if len(admins) == 1:
        print(f"Using local administrator '{admins[0]}' for sample data.")
        return admins[0]
    if not sys.stdin.isatty():
        raise CommandError("Seed needs --manager with an existing active username, or an interactive terminal to create/select one.")
    if admins:
        print("Multiple administrators found. Enter the local username to use for sample data.")
        username = input("Manager username: ").strip()
        if not username:
            raise CommandError("Manager username cannot be empty. Rerun with --manager USERNAME.")
        return resolve_manager(username)
    print("No active administrator found. Create a local administrator to seed sample data.")
    call_command("createsuperuser", interactive=True)
    return resolve_manager()


def odbc_value(value):
    return "{" + value.replace("}", "}}") + "}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server")
    parser.add_argument("--database")
    parser.add_argument("--driver")
    seed_options = parser.add_mutually_exclusive_group()
    seed_options.add_argument("--seed-demo", dest="seed_demo", action="store_true", help="Seed fictional data (default).")
    seed_options.add_argument("--no-seed-demo", dest="seed_demo", action="store_false", help="Only create database and apply migrations.")
    parser.set_defaults(seed_demo=True)
    parser.add_argument("--manager")
    parser.add_argument("--basic-demo", action="store_true", help="Use the original small acceptance dataset instead of the full demo.")
    args = parser.parse_args()
    if not args.seed_demo and args.manager:
        parser.error("--manager cannot be used with --no-seed-demo.")
    if not args.seed_demo and args.basic_demo:
        parser.error("--basic-demo cannot be used with --no-seed-demo.")

    env_path = ROOT / ".env"
    local_config = dotenv_values(env_path)
    config = {**dotenv_values(ROOT / ".env.example"), **local_config}
    # Explicit parameters override environment variables, which override the local file.
    for key in config:
        config[key] = os.environ.get(key, config[key])
    if args.server:
        config["DT05_SQL_HOST"] = args.server
    if args.database:
        config["DT05_SQL_DATABASE"] = args.database
    installed = pyodbc.drivers()
    driver = args.driver or config.get("DT05_SQL_DRIVER")
    if not args.driver and driver not in installed:
        driver = next(
            (name for name in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]
             if name in installed),
            None,
        )
    if driver not in installed:
        raise ValueError("Install Microsoft ODBC Driver 17/18 or specify an installed --driver.")
    config["DT05_SQL_DRIVER"] = driver
    database = config["DT05_SQL_DATABASE"]
    if not database or len(database) > 128:
        raise ValueError("Database name must contain 1 to 128 characters.")
    if database.lower() in {"master", "tempdb", "model", "msdb"}:
        raise ValueError("Choose a project database instead of a SQL Server system database.")
    if not config.get("DJANGO_SECRET_KEY") or config["DJANGO_SECRET_KEY"] == "replace-with-a-local-random-key":
        config["DJANGO_SECRET_KEY"] = secrets.token_urlsafe(48)

    parts = {
        "DRIVER": driver,
        "SERVER": config["DT05_SQL_HOST"],
        "DATABASE": "master",
        "Encrypt": config["DT05_SQL_ENCRYPT"],
        "TrustServerCertificate": config["DT05_SQL_TRUST_CERTIFICATE"],
    }
    if config.get("DT05_SQL_USER"):
        parts.update(UID=config["DT05_SQL_USER"], PWD=config.get("DT05_SQL_PASSWORD", ""))
    else:
        parts["Trusted_Connection"] = "yes"
    connection_string = ";".join(f"{key}={odbc_value(value)}" for key, value in parts.items())
    connection = pyodbc.connect(connection_string, autocommit=True, timeout=5)
    try:
        cursor = connection.cursor()
        if cursor.execute("SELECT DB_ID(?)", database).fetchval() is None:
            quoted_name = "[" + database.replace("]", "]]") + "]"
            cursor.execute("CREATE DATABASE " + quoted_name)
            print(f"Created database {database}.")
        else:
            print(f"Using existing database {database}.")
    finally:
        connection.close()

    for key, value in config.items():
        if local_config.get(key) != (value or ""):
            set_key(str(env_path), key, value or "")
        os.environ[key] = value or ""
    load_dotenv(env_path)
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django
    from django.core.management import call_command

    django.setup()
    call_command("migrate", interactive=False)
    call_command("check", databases=["default"])
    if args.seed_demo:
        if args.basic_demo:
            call_command("seed_demo", manager=resolve_manager(args.manager))
        else:
            call_command("seed_demo", full=True, manager=args.manager)
            call_command("check_demo_data", manager=args.manager)
    print("Database setup completed. Local configuration is saved in .env.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # SQL drivers may echo the connection string. Remove its password before reporting.
        message = str(error)
        password = os.environ.get("DT05_SQL_PASSWORD") or dotenv_values(ROOT / ".env").get("DT05_SQL_PASSWORD")
        if password:
            message = message.replace(password, "***")
        message = re.sub(r"(?i)(PWD|PASSWORD)=([^;]*)", r"\1=***", message)
        print(f"Database setup failed: {message}", file=sys.stderr)
        sys.exit(1)
