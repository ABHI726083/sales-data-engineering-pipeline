import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOG FILE
# ============================================================

LOG_FILE = LOG_DIR / "pipeline.log"


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger("data_pipeline")

logger.setLevel(logging.INFO)

logger.propagate = False


# ============================================================
# PREVENT DUPLICATE HANDLERS
# ============================================================

if not logger.handlers:

    # ========================================================
    # ROTATING FILE HANDLER
    # ========================================================

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)

    # ========================================================
    # LOG FORMAT
    # ========================================================

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    # ========================================================
    # ADD FILE HANDLER
    # ========================================================

    logger.addHandler(file_handler)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def log_info(message, *args):
    logger.info(message, *args)


def log_warning(message, *args):
    logger.warning(message, *args)


def log_error(message, *args):
    logger.error(message, *args)


def log_exception(message, *args):
    logger.exception(message, *args)