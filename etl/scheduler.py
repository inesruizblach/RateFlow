"""
scheduler.py — Automate the RateFlow ETL pipeline
Runs extract + load at a regular interval using the schedule library.
"""

import time
import subprocess
import schedule
from datetime import datetime

def run_etl():
    print(f"🕒 Running ETL at {datetime.utcnow().isoformat()} UTC...")
    subprocess.run(["python", "etl/load.py"])
    print("✅ ETL completed successfully!\n")

# --- Schedule the job ---
schedule.every().day.at("09:00").do(run_etl)

print("🚀 RateFlow ETL Scheduler started. Running every day at 9am...")

# --- Keep the scheduler alive ---
while True:
    schedule.run_pending()
    time.sleep(60)
