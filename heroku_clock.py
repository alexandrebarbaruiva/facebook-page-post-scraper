from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages
from scraper.token_manager import collect_token

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():
	print("test")
	csv_dir = home.joinpath('csv')
	json_dir = home.joinpath('json')
	if not csv_dir.is_dir():
		csv_dir.mkdir()
	if not json_dir.is_dir():
		json_dir.mkdir()

	#collect_token()
	#collect_all_pages()

sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=21, minute=32)


#@sched.scheduled_job('interval', minutes=3)
#def timed_job():
    #print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21, minute=33)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    csv_dir = home.joinpath('csv')
    json_dir = home.joinpath('json')
    if not csv_dir.is_dir():
    	csv_dir.mkd()
    if not json_dir.is_dir():
    	json_dir.mkdir()


sched.start()