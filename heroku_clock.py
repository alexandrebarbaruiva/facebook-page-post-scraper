"""

@heroku_clock é o resposável pela configuração do agendamento de execusão do modulo
scraper/collector.py que chama a função collect_all_pages().

"""

from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():
	""" Função principal do agendador """
	print("Início do coleta de dados")
	collect_all_pages()
	print("Fim do coleta de dados")


sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=11, minute=2)
""" Configuração básica dos dias da semana e do horário que a função será executada """

sched.start()