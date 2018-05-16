#from apschedule.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
from scraper import collector

sched = BlockingScheduler()

def job_function():
	print("teste")
	collector.collect_all_pages()

sched.add_job(job_function,'cron', day_of_week='mon-fri', hour=16, minute=56)

def schedule_job():
	collector.collect_all_pages()



sched.start()
