from main import main
import schedule
import time

schedule.every(30).day.at("22:00")

while True:
    schedule.run_pending()
    time.sleep(1)