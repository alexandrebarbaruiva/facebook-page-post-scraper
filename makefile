JsonDir = ./json/
CsvDir = ./csv/
UNAME := $(shell uname)
face_file1 = venv/src/facebook-sdk/facebook/__init__.py
face_file2 = venv/src/facebook-sdk/facebook/version.py

default: test

travis:
	green3 tests.test_page_scraper.TestPageScraperBasics -vvv

test:
ifeq ($(OS), Windows_NT)
	green3 -vv
else
	green3 -vvv
endif

run:
ifeq ($(OS), Windows_NT)
	python scraper\collector.py
else
	python3 scraper/collector.py
endif

tm:
ifeq ($(OS), Windows_NT)
	green3 tests\test_token_manager.py -vv
else
	green3 tests/test_token_manager.py -vvv -f
endif

ps:
ifeq ($(OS), Windows_NT)
	green3 tests\test_page_scraper.py -vv
else
	green3 tests/test_page_scraper.py -vvv -f
endif

style:
ifeq ($(OS), Windows_NT)
	pycodestyle tests\. scraper\.
else
	pycodestyle tests/. scraper/.
endif

cov:
ifeq ($(OS), Windows_NT)
	coverage run -m py.test tests\test_page_scraper.py
	coverage report -m scraper\page_scraper.py
	coverage html scraper\page_scraper.py
else
	coverage run -m py.test tests/test_page_scraper.py
	coverage report -m scraper/page_scraper.py
	coverage html scraper/page_scraper.py
endif

full:
ifeq ($(OS), Windows_NT)
	make clean
	green3 -vvv --run-coverage -o $(face_file1),$(face_file2)
	coverage html scraper\page_scraper.py scraper\token_manager.py
	make style
else
	make clean
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
	python3 scraper/token_manager.py

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
	rm -f .\*.json
	rm -f .\json\*.json
	rm -f .\csv\*.csv
	rm -rf .\htmlcov
	rm -f .\.coverage
else
	rm -f ./*.json
	rm -f $(JsonDir)*.json
	rm -f $(CsvDir)*.csv
	rm -rf ./htmlcov
	rm -f ./.coverage
endif

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
	@echo "\n\t End of Makefile Help\n"
endif
