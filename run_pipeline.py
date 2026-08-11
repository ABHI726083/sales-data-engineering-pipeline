import sys
import os
import subprocess
import time
from pathlib import Path

from utils.logger import (
    log_info,
    log_error,
    log_exception
)

# ============================================================
# FORCE UTF-8 OUTPUT
# ============================================================

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(
        encoding="utf-8"
    )

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(
        encoding="utf-8"
    )

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# ============================================================
# CHECK INPUT ARGUMENT
# ============================================================

if len(sys.argv) < 2:

    print("ERROR: Please provide a CSV file path.")
    print("Example:")
    print("python run_pipeline.py data/sales.csv")

    log_error(
        "No input CSV file provided."
    )

    sys.exit(1)

# ============================================================
# GET INPUT FILE
# ============================================================

input_file = Path(sys.argv[1])

if not input_file.is_absolute():

    input_file = PROJECT_ROOT / input_file

input_file = input_file.resolve()

print(
    "Input CSV:",
    input_file
)

log_info(
    f"Input CSV: {input_file}"
)

# ============================================================
# CHECK INPUT FILE
# ============================================================

if not input_file.is_file():

    print(
        "\nERROR: Input CSV file not found!"
    )

    print(
        "File:",
        input_file
    )

    log_error(
        f"Input CSV file not found: {input_file}"
    )

    sys.exit(1)

# ============================================================
# LOG + PRINT MESSAGE
# ============================================================

def log_message(message):

    print(message)

    log_info(message)

# ============================================================
# RUN PIPELINE STEP
# ============================================================

def run_step(step_name, command):

    print(
        "\n" + "=" * 50
    )

    print(step_name)

    print(
        "=" * 50
    )

    log_info("=" * 50)
    log_info(step_name)
    log_info("=" * 50)

    start_time = time.time()

    try:

        # ====================================================
        # CREATE ENVIRONMENT FOR CHILD PROCESS
        # ====================================================

        child_env = os.environ.copy()

        existing_pythonpath = child_env.get(
            "PYTHONPATH",
            ""
        )

        if existing_pythonpath:

            child_env["PYTHONPATH"] = (
                str(PROJECT_ROOT)
                + os.pathsep
                + existing_pythonpath
            )

        else:

            child_env["PYTHONPATH"] = str(
                PROJECT_ROOT
            )

        # ====================================================
        # RUN CHILD PROCESS
        # ====================================================

        result = subprocess.run(
            [sys.executable] + command,
            cwd=PROJECT_ROOT,
            env=child_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # ====================================================
        # SAVE CHILD STDOUT TO LOG
        # ====================================================

        if result.stdout:

            print(
                result.stdout,
                end=""
            )

            log_info(
                f"OUTPUT FROM {step_name}:\n"
                f"{result.stdout.rstrip()}"
            )

        # ====================================================
        # SAVE CHILD STDERR TO LOG
        # ====================================================

        if result.stderr:

            print(
                result.stderr,
                end=""
            )

            log_error(
                f"ERROR OUTPUT FROM {step_name}:\n"
                f"{result.stderr.rstrip()}"
            )

        # ====================================================
        # CHECK RETURN CODE
        # ====================================================

        if result.returncode != 0:

            execution_time = (
                time.time()
                - start_time
            )

            print(
                f"\nERROR: {step_name} FAILED!"
            )

            print(
                f"Execution time: "
                f"{execution_time:.2f} seconds"
            )

            log_error(
                f"{step_name} FAILED!"
            )

            log_error(
                f"Return code: {result.returncode}"
            )

            log_error(
                f"Execution time: "
                f"{execution_time:.2f} seconds"
            )

            print(
                "\nPipeline stopped."
            )

            log_error(
                "Pipeline stopped."
            )

            sys.exit(
                result.returncode
            )

        # ====================================================
        # SUCCESS
        # ====================================================

        execution_time = (
            time.time()
            - start_time
        )

        print(
            f"\nSTEP: {step_name} "
            f"completed successfully!"
        )

        print(
            f"Execution time: "
            f"{execution_time:.2f} seconds"
        )

        log_info(
            f"{step_name} completed successfully!"
        )

        log_info(
            f"Execution time: "
            f"{execution_time:.2f} seconds"
        )

    except Exception as error:

        execution_time = (
            time.time()
            - start_time
        )

        print(
            f"\nERROR: {step_name} FAILED!"
        )

        print(
            f"Unexpected error: {error}"
        )

        print(
            f"Execution time: "
            f"{execution_time:.2f} seconds"
        )

        log_exception(
            f"{step_name} failed with unexpected error."
        )

        log_error(
            f"Unexpected error: {error}"
        )

        log_error(
            f"Execution time: "
            f"{execution_time:.2f} seconds"
        )

        print(
            "\nPipeline stopped."
        )

        sys.exit(1)

# ============================================================
# PIPELINE START
# ============================================================

pipeline_start_time = time.time()

log_message(
    "\nPIPELINE STARTED"
)

log_message(
    f"Input CSV: {input_file}"
)

# ============================================================
# STEP 1: LOAD RAW DATA
# ============================================================

run_step(
    "STEP 1: LOAD RAW DATA",
    [
        "src/load_data.py",
        str(input_file)
    ]
)

# ============================================================
# STEP 2: CLEAN DATA
# ============================================================

run_step(
    "STEP 2: CLEAN DATA",
    [
        "src/clean_data.py",
        str(input_file)
    ]
)

# ============================================================
# STEP 3: VALIDATE CLEANED DATA
# ============================================================

cleaned_file = (
    PROJECT_ROOT
    / "output"
    / "cleaned_sales.csv"
)

run_step(
    "STEP 3: VALIDATE DATA",
    [
        "src/validate_data.py",
        str(cleaned_file)
    ]
)

# ============================================================
# STEP 4: LOAD INTO POSTGRESQL
# ============================================================

run_step(
    "STEP 4: LOAD INTO POSTGRESQL",
    [
        "database/load_to_db.py"
    ]
)

# ============================================================
# STEP 5: RUN ANALYTICS
# ============================================================

run_step(
    "STEP 5: RUN ANALYTICS",
    [
        "src/analytics.py"
    ]
)

# ============================================================
# STEP 6: GENERATE REPORTS
# ============================================================

run_step(
    "STEP 6: GENERATE REPORTS",
    [
        "src/generate_reports.py"
    ]
)

# ============================================================
# PIPELINE COMPLETE
# ============================================================

total_time = (
    time.time()
    - pipeline_start_time
)

print(
    "\n" + "=" * 50
)

print(
    "PIPELINE COMPLETED SUCCESSFULLY!"
)

print(
    "=" * 50
)

print(
    f"Total pipeline execution time: "
    f"{total_time:.2f} seconds"
)

# ============================================================
# FINAL LOGGING
# ============================================================

log_info(
    "PIPELINE COMPLETED SUCCESSFULLY"
)

log_info(
    f"Total pipeline execution time: "
    f"{total_time:.2f} seconds"
)