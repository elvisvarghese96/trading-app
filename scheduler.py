import schedule
import time
from script import fetch_and_store_tickers


def running_job():
    print("Running the job...")

#schedule.every().day.at("12:00").do(running_job)
schedule.every().minute.do(running_job)

# Schedule the job for every day at midnight
#schedule.every().day.at("12:00").do(fetch_and_store_tickers)

# Schedule the job for every minute
schedule.every().minute.do(fetch_and_store_tickers)

print("Scheduler started... waiting for job to start")
while True:
    schedule.run_pending()
    time.sleep(10)                  # check 10 seconds


