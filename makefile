JsonDir = ./json/
UNAME := $(shell uname)

default: tm

test:
	green3 . -vvv

run:
	python3 scraper/collector.py

tm:
	green3 tests/test_token_manager.py -vvv

install:
	pip3 install -r requirements.txt

style:
	pycodestyle scraper/ tests/

cov:
	coverage run -m py.test tests/test.py
	coverage report -m scraper/post_scraper.py
	coverage report -m scraper/token_manager.py
	coverage html scraper/post_scraper.py

full:
	make test
	make cov
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
	@echo " make.............= Runs the tests using green3"
	@echo " make test........= Also runs the tests using green3"
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
