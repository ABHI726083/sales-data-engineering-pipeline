import subprocess
import sys
import time
import webbrowser
import urllib.request
import urllib.error


# ============================================================
# APPLICATION URLs
# ============================================================

API_URL = "http://127.0.0.1:8000"
DOCS_URL = f"{API_URL}/docs"
DASHBOARD_URL = "http://127.0.0.1:8501"


# ============================================================
# WAIT FOR FASTAPI
# ============================================================

def wait_for_api(timeout=30):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(API_URL, timeout=2)
            return True

        except urllib.error.HTTPError:
            # FastAPI is running even if the endpoint returns 404/405
            return True

        except Exception:
            time.sleep(1)

    return False


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("=" * 50)
    print("DATA PIPELINE APPLICATION")
    print("=" * 50)

    # --------------------------------------------------------
    # START FASTAPI
    # --------------------------------------------------------

    print("\nStarting FastAPI...")

    api_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api.app:app",
            "--reload",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ]
    )

    print("Waiting for FastAPI...")

    if not wait_for_api():

        print("\nERROR: FastAPI could not be started.")

        api_process.terminate()

        return

    print("FastAPI started successfully!")
    print(f"API Docs: {DOCS_URL}")

    # --------------------------------------------------------
    # START STREAMLIT DASHBOARD
    # --------------------------------------------------------

    print("\nStarting Streamlit dashboard...")

    dashboard_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard/app.py",
            "--server.port",
            "8501",
        ]
    )

    # Give Streamlit time to start
    time.sleep(3)

    # --------------------------------------------------------
    # OPEN BROWSER
    # --------------------------------------------------------

    print("\nOpening application...")

    webbrowser.open(DOCS_URL)

    webbrowser.open(DASHBOARD_URL)

    # --------------------------------------------------------
    # APPLICATION INFORMATION
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("APPLICATION RUNNING")
    print("=" * 50)

    print(f"FastAPI Docs : {DOCS_URL}")
    print(f"Dashboard    : {DASHBOARD_URL}")

    print("\nPress Ctrl+C to stop.")

    # --------------------------------------------------------
    # KEEP APPLICATION RUNNING
    # --------------------------------------------------------

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping application...")

        # Stop FastAPI
        api_process.terminate()

        # Stop Streamlit
        dashboard_process.terminate()

        print("Application stopped.")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()