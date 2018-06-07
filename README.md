# Facebook Scraper

**[:brazil: Readme](./README.md) | [:us: Readme](./.github/Readme/Language/English/README.md)**

[![Build Status](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper.svg?branch=master)](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d78fb4221b49847ca9c/maintainability)](https://codeclimate.com/github/unb-cic-esw/facebook-page-post-scraper/maintainability)

## Fazendo tudo rodar 

Uma vez que se tenha instalado python 3 e Git, baixado o repositório e
esteja com um editor de texto adequado (Atom, VSCode, Sublime ou Pycharm), deve-se
seguir os seguintes passos

Criar o ambiente virtual (venv) e entrar no mesmo

```
python3 -m venv venv
source venv/bin/activate
```

Para aqueles no Linux ou Mac

```
make install
```

Para windows

```
pip install -r requirements.txt
```

Uma vez instalados todos os módulos, é necessário configurar o token.
Para isso devemos baixar o ChromeDriver. Para Linux e MacOS basta utilizar o comando

```
make chromedriver
```

Para Windows, é necessário seguir as instruções do Splinter para Windows:
([Instruções para baixar ChromeDriver](https://splinter.readthedocs.io/en/latest/drivers/chrome.html)).
Uma vez com o ChromeDriver instalado corretamente,para a aquisição do Token basta digitar

```
make autotoken
```

## Usando o Programa

Uma vez com todas as configurações feitas, use:

```
make run
```

## Rodando testes

Por enquanto rodar testes é a principal funcionalidade. Em breve serão adicionadas 
mais funções. Portanto, para testes

```
make
```

E para saber qual a cobertura dos testes, use

```
make cov
```

## Verificando estilo

Para verificar se o seu código encontra-se bem indentado e bonito, use o seguinte comando

```
make style
```

Importante usar este comando antes de mandar uma PR para garantir código mais legível..

## Heroku

O Heroku é uma das mais populares de plataforma como serviço que suporta
aplicações escritas em diversas linguagens, dentre elas, Python, java, node, etc.

Primeiro precisa criar uma conta.

requirements.txt - especifica todas as dependencias que a aplicação
precisa para rodar dentro do Heroku.

Procfile - especifica os comandos que serão executados pela aplicação
dentro da máquina Dynos. Nossa aplicação é um serviço de coleta de
dados que será todos dias da semana em um horário especifico.
Formato do arquivo:
clock: python heroku_clock.py

runtime.txt - especifica a versão do python que é suportada pela aplicação.
python-3.5.2

Link Heroku - ([facebook-page-post-scraper](https://dashboard.heroku.com/apps/facebook-page-post-scraper)).

Clone do repositorio:
heroku git:clone -a facebook-page-post-scraper

Adicionar um remote:

```
heroku login
git remote add heroku https://git.heroku.com/facebook-page-post-scraper.git
git pull heroku master
```

Link Heroku - Git ([Deploying with Git](https://devcenter.heroku.com/articles/git)).

Link Heroku - Agendamento ([Scheduled (Agendamento)](https://devcenter.heroku.com/articles/scheduled-jobs-custom-clock-processes)).

## APScheduled

É uma biblioteca em python que permite realizar agendamento de tarefas (jobs). ([APScheduled](http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html)).

## Agendamento

python heroku_clock.py

## Um projeto de


[![alt text][unb]](https://www.unb.br/)

[unb]:./.github/Images/logo_unb.png

Universidade de Brasília


[![alt text][resocie]](https://www.resocie.org/)

[resocie]:./.github/Images/resocie.jpg

Resocie : Repensando as Relações entre Sociedade e Estado

