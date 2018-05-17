from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages

sched = BlockingScheduler()

def job_function():
	print("test")
	collect_all_pages()

sched.add_job(job_function,'cron', day_of_week='mon-fri', hour=9, minute=38)

sched.start()