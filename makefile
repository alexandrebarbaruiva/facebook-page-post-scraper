JsonDir = ./json/
UNAME := $(shell uname)

default: test

test:
	green3 . -vvv

run:
	python3 -m scraper/post_scraper.py

collect:
	python3 scraper/collector.py

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
else
	ifeq ($(UNAME), Darwin)
		brew install chromedriver
	endif
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
	@echo " make test........= Also run the tests using green3"
	@echo " make run.........= Run post_scrapper.py"
	@echo " make install.....= Install the requirements necessary for this project"
	@echo " make style.......= Cheks if your code is our pattern of coding for this project"
	@echo " make json........= Creates a json dir and moves all .json files there"
	@echo " make cov.........= Checks how much our program is coverage"
	@echo " make full........= Runs make test, cov and style"
	@echo " make autotoken...= Open Facebook Developers web page so that the user can "
	@echo "                    take a new token and update config.ini file"
	@echo " make json........= Creates a json dir and moves all .json files there"
	@echo " make clean.......= Removes all .json files"
	@echo " make createconfig= Creates config.ini in scraper dir with the expected way to use it"
	@echo " make chromedriver.= Install chromedriver for get the token automatically, works in"
	@echo "                    Linux and MacOS"
	@echo "\n\t End of Makefile Help\n"
