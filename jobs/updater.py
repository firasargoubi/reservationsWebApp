from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  
from .jobs import job

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds = 1,start_date='2024-09-07 15:05:00')
    scheduler.start()
