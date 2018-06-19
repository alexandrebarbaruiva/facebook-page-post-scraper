from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages, collect_new_data

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():

	print("Início do coleta de dados")
	collect_all_pages()
	# collect_new_data()
	print("Fim do coleta de dados")

sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=13, minute=4)

sched.start()