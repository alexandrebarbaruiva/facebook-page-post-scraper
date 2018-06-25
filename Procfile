# O Procfile que especifica os comandos que são executados pelos dynos do aplicativo.
# Nossa aplicação usa dois serviços:
#
# web: Um servidor para disponibilizar informações na web do projeto utilizando o ambiente gunicorn;
# clock: Um servidor de agendamento que utilizar um ambiente apscheduler.  
#
# Formato do Procfile:
# <process type>: <command>
#

web: gunicorn __init__:app 
clock: python -m heroku_clock
