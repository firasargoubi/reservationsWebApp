from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  
from .jobs import job

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', hours = 24,start_date='2024-09-08 8:00:00')
    scheduler.start()
