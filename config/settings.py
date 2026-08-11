import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR = BASE_DIR / "output"

REPORTS_DIR = OUTPUT_DIR / "reports"

LOGS_DIR = BASE_DIR / "logs"


# ============================================================
# FILE PATHS
# ============================================================

CLEANED_DATA_FILE = (
    OUTPUT_DIR / "cleaned_sales.csv"
)

PIPELINE_LOG_FILE = (
    LOGS_DIR / "pipeline.log"
)


# ============================================================
# DATABASE SETTINGS
# ============================================================

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_PORT = os.getenv(
    "DB_PORT",
    "5432"
)

DB_NAME = os.getenv(
    "DB_NAME"
)

DB_USER = os.getenv(
    "DB_USER"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD"
)


# ============================================================
# VALIDATE DATABASE CONFIGURATION
# ============================================================

REQUIRED_DB_SETTINGS = {
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}


missing_db_settings = [
    name
    for name, value in REQUIRED_DB_SETTINGS.items()
    if not value
]


if missing_db_settings:

    raise RuntimeError(
        "Missing required database environment "
        "variables: "
        + ", ".join(missing_db_settings)
    )


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

for directory in [
    DATA_DIR,
    OUTPUT_DIR,
    REPORTS_DIR,
    LOGS_DIR,
]:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )