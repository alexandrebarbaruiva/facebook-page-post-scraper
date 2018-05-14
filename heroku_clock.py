from apschedule.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_weed='mon-fri', hour=21, min=11)
def schedule_job():
	from .scraper import collector
	collector.collect_all_pages()

sched.start()