import schedule
import time
import subprocess

def run_etl():
    print("Running ETL pipeline...")
    subprocess.run(["python", "etl/load.py"])

# Run every day at 09:00
schedule.every().day.at("09:00").do(run_etl)

print("Scheduler running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
