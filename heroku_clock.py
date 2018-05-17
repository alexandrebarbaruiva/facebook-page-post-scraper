from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages
from scraper.token_manager import collect_token

sched = BlockingScheduler()

def job_function():
	print("test")
	collect_token()
	collect_all_pages()

sched.add_job(job_function,'cron', day_of_week='mon-fri', hour=19, minute=28)

sched.start()