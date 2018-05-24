from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages
from scraper.token_manager import collect_token_automatically

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():
	collect_token_automatically()
	collect_all_pages()

sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=12, minute=00)

sched.start()