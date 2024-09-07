from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  
from .jobs import job

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds = 10,start_date='2024-09-07 15:10:00')
    scheduler.start()
