from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler  
from .jobs import job

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds = 5)
    scheduler.start()
