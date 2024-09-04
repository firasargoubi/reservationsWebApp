from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  
from .jobs import job

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', hour = 8,minute = 0)
    scheduler.start()