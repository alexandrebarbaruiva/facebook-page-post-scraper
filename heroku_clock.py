from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages
from scraper.token_manager import collect_token
#from scraper.new_data_collector import collect_new_data

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():
	# print("coletando\n")
	collect_all_pages()
	#collect_new_data()

sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=8, minute=00)

sched.start()