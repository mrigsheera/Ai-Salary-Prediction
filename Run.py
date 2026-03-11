import subprocess
import sys
import os
import time
import webbrowser

# ─── Get the folder where this script lives ───────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_FILE  = os.path.join(BASE_DIR, "api.py")
APP_FILE  = os.path.join(BASE_DIR, "APP.py")

print("=" * 50)
print("   AI Salary Predictor — Launcher")
print("=" * 50)

# ─── Start Flask API ──────────────────────────────────────────────────────────
print("\n[1/2] Starting Flask API on http://localhost:5000 ...")
api_process = subprocess.Popen(
    [sys.executable, API_FILE],
    cwd=BASE_DIR,
)
time.sleep(3)  # Give Flask time to load & train the model
print("      ✅ Flask API started!")

# ─── Start Streamlit ──────────────────────────────────────────────────────────
print("\n[2/2] Starting Streamlit UI on http://localhost:8501 ...")
streamlit_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", APP_FILE,
     "--server.headless", "true",
     "--browser.gatherUsageStats", "false"],
    cwd=BASE_DIR,
)
time.sleep(3)
print("      ✅ Streamlit started!")

# ─── Open browser ─────────────────────────────────────────────────────────────
print("\n🚀 Opening browser at http://localhost:8501 ...\n")
webbrowser.open("http://localhost:8501")

print("=" * 50)
print("  Both servers are running!")
print("  Press Ctrl+C to stop everything.")
print("=" * 50)

# ─── Keep running until Ctrl+C ────────────────────────────────────────────────
try:
    api_process.wait()
except KeyboardInterrupt:
    print("\n\nShutting down...")
    api_process.terminate()
    streamlit_process.terminate()
    print("✅ All servers stopped. Goodbye!")