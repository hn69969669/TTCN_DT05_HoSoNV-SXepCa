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


def odbc_value(value):
    return "{" + value.replace("}", "}}") + "}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server")
    parser.add_argument("--database")
    parser.add_argument("--driver")
    parser.add_argument("--seed-demo", action="store_true")
    parser.add_argument("--manager")
    args = parser.parse_args()
    if args.seed_demo and not args.manager:
        parser.error("--seed-demo requires --manager with an existing local username.")

    env_path = ROOT / ".env"
    config = {**dotenv_values(ROOT / ".env.example"), **dotenv_values(env_path)}
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
        call_command("seed_demo", manager=args.manager)
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
