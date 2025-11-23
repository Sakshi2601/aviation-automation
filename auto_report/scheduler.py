import schedule
import time
import os
from main import run_pipeline


def job():
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, "data", "input.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base, "data", "flights.csv")

    print("Running scheduled pipeline...")
    try:
        run_pipeline(
            csv_path,
            out_pdf=os.path.join(base, "reports", "output_report.pdf")
        )
        print("Scheduled run completed successfully.")
    except Exception as e:
        print("Scheduled run failed:", e)


if __name__ == "__main__":
    # Run every day at 7:00 AM
    schedule.every().day.at("07:00").do(job)

    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
