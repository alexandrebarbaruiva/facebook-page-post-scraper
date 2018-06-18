JsonDir = ./json/
CsvDir = ./csv/
UNAME := $(shell uname)
face_file1 = venv/src/facebook-sdk/facebook/__init__.py
face_file2 = venv/src/facebook-sdk/facebook/version.py

default: test

travis:
	@make style

test:
ifeq ($(OS), Windows_NT)
	make clean
	green3 -vv
else
	@make clean
	green3 -vv
endif

data:
	python3 -c 'from scraper.collector import collect_new_data; collect_new_data()'

run:
ifeq ($(OS), Windows_NT)
	python -m scraper\collector
else
	mkdir -p $(JsonDir)
	mkdir -p $(CsvDir)
	python3 -m scraper.collector
endif

heroku:
ifeq ($(OS), Windows_NT)
	python3 -m heroku_clock
else
	python3 -m heroku_clock
endif

tm:
ifeq ($(OS), Windows_NT)
	green3 tests\test_token_manager.py -vv
else
	green3 tests/test_token_manager.py -vvv -f
endif

ps:
ifeq ($(OS), Windows_NT)
	make clean
	green3 tests\test_page_scraper.py -vv
else
	make clean
	green3 tests/test_page_scraper.py -vvv -f
endif

style:
ifeq ($(OS), Windows_NT)
	pycodestyle tests\. scraper\. server/. --ignore=E402,W504
else
	pycodestyle tests/. scraper/. server/. --ignore=E402,W504
endif

cov:
ifeq ($(OS), Windows_NT)
	make clean
	coverage run -m py.test tests/test_page_scraper.py tests/test_token_manager.py
	coverage report -m scraper/page_scraper.py scraper/token_manager.py
	coverage html scraper/page_scraper.py scraper/token_manager.py
else
	make clean
	coverage run -m py.test tests/test_page_scraper.py tests/test_token_manager.py
	coverage report -m scraper/page_scraper.py scraper/token_manager.py
	coverage html scraper/page_scraper.py scraper/token_manager.py
endif

full:
ifeq ($(OS), Windows_NT)
	make clean
	green3 -vvv --run-coverage -o $(face_file1),$(face_file2)
	coverage html scraper\page_scraper.py scraper\token_manager.py
	make style
else
	@make clean
	green3 -vvv --run-coverage -f -o $(face_file1),$(face_file2)
	coverage html scraper/page_scraper.py scraper/token_manager.py
	make style
endif

cc:
	radon cc scraper -s

mi:
	radon mi scraper -s

install:
	pip3 install -r requirements.txt

.PHONY: autotoken
autotoken:
	python3 -m scraper.token_manager

.PHONY: chromedriver
chromedriver:
ifeq ($(UNAME), Linux)
	cd $(HOME)/Downloads
	wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	mkdir -p $(HOME)/bin
	mv chromedriver $(HOME)/bin
	echo "export PATH=$(PATH):$(HOME)/bin" >> $(HOME)/.bash_profile
	rm -f chromedriver_linux64.zip
endif

# Call for creating a Json dir and moves all json files there
.PHONY: json
json:
	mkdir -p $(JsonDir)
	mv *.json $(JsonDir); true

# Call for *.json clean up
.PHONY: clean
clean:
ifeq ($(OS), Windows_NT)
	rm -f .\csv\*.csv
	rm -rf .\htmlcov
	rm -f .\.coverage
	rm -f .\json
else
	rm -f $(CsvDir)*.csv
	rm -rf ./htmlcov
	rm -f ./.coverage
	rm -rf ./json/
endif

pylint:
	pylint -j 2 scraper/page_scraper.py scraper/token_manager.py --reports=y

# Call for *.json clean up
.PHONY: createconfig
createconfig:
	echo '[DEFAULT]\ntoken = YOURTOKENHERE' >./scraper/config.ini


# Call for help with this makefile's commands
.PHONY: help
help:
ifeq ($(OS), Windows_NT)
	@echo.
	@echo     Makefile of Facebook scrapper from UnB
	@echo.
	@echo  make.............= Runs the default function
	@echo  make test........= Runs the tests using green3
	@echo  make tm..........= Runs only the tests on token management
	@echo  make ps..........= Runs only the tests on page scraping
	@echo  make run.........= Collects all pages in entidades.csv
	@echo  make install.....= Installs the requirements necessary for this project
	@echo  make style.......= Checks if your code is our pattern of coding for this
	@echo                     project
	@echo  make json........= Creates a json dir and moves all .json files there
	@echo  make cov.........= Checks tests coverage
	@echo  make full........= Runs make test, cov and style
	@echo  make autotoken...= Open Facebook Developers web page so that the user can
	@echo                     take a new token and update config.ini file
	@echo  make json........= Creates a json dir and moves all .json files there
	@echo  make clean.......= Removes all .json files
	@echo  make createconfig= Creates config.ini in scraper dir with the expected way
	@echo                     to use it
	@echo  make chromedriver= Install chromedriver for get the token automatically,
	@echo                     works in Linux
	@echo  make heroku......= Realiza o agendamento do serviço de coleta de dados
	@echo                     diariamente. A configuração é feita no arquivo heroku_clock.
	@echo.
	@echo      End of Makefile Help
	@echo.
else
	@echo "\n\t Makefile of Facebook scrapper from UnB\n"
	@echo " make.............= Runs the default function"
	@echo " make test........= Runs the tests using green3"
	@echo " make tm..........= Runs only the tests on token management"
	@echo " make ps..........= Runs only the tests on page scraping"
	@echo " make run.........= Collects all pages in entidades.csv"
	@echo " make install.....= Installs the requirements necessary for this project"
	@echo " make style.......= Checks if your code is our pattern of coding for this "
	@echo "                    project"
	@echo " make json........= Creates a json dir and moves all .json files there"
	@echo " make cov.........= Checks test's coverage"
	@echo " make full........= Runs make test, cov and style"
	@echo " make autotoken...= Open Facebook Developers web page so that the user can "
	@echo "                    take a new token and update config.ini file"
	@echo " make json........= Creates a json dir and moves all .json files there"
	@echo " make clean.......= Removes all .json files"
	@echo " make createconfig= Creates config.ini in scraper dir with the expected way"
	@echo "                    to use it"
	@echo " make chromedriver= Install chromedriver for get the token automatically, "
	@echo "                    works in Linux"
	@echo " make heroku......= Realiza o agendamento do serviço de coleta de dados"
	@echo "                    diariamente. A configuração é feita no arquivo heroku_clock."
	@echo "\n\t End of Makefile Help\n"
endif
