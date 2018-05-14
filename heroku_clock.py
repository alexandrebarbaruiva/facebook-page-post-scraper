from apschedule.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_weed='mon-fri', hour=20, min=07)
def schedule_job():
	from .scraper import collector
	collector.collect_all_pages()

sched.start()