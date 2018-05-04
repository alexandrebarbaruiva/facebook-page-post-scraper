JsonDir = ./json/
CsvDir = ./csv/
UNAME := $(shell uname)
face_file1 = venv/src/facebook-sdk/facebook/__init__.py
face_file2 = venv/src/facebook-sdk/facebook/version.py

default: test

test:
	green -vv

run:
	python scraper\collector.py

tm:
	green3 tests\test_token_manager.py -vvv

ps:
	green3 tests/test_page_scraper.py -vvv

install:
	pip3 install -r requirements.txt

style:
	pycodestyle scraper/ tests/

cov:
	coverage run -m py.test tests/test_page_scraper.py tests/test_token_manager.py
	coverage report -m scraper/page_scraper.py scraper/token_manager.py
	coverage html scraper/page_scraper.py scraper/token_manager.py

full:
	make clean
	green3 -vvv --run-coverage -o $(face_file1),$(face_file2)
	coverage html scraper/page_scraper.py scraper/token_manager.py
	make style

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
	rm -f ./*.json
	rm -f $(JsonDir)*.json
	rm -f $(CsvDir)*.csv
	rm -rf ./htmlcov
	rm -f ./.coverage

# Call for *.json clean up
.PHONY: createconfig
createconfig:
	echo '[DEFAULT]\ntoken = YOURTOKENHERE' >./scraper/config.ini


# Call for help with this makefile's commands
.PHONY: help
help:
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
