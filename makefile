default: test

test:
	green3 . -vvv

run:
	python3 scraper/post_scraper.py

install:
	pip3 install -r requirements.txt

style:
	pycodestyle scraper/ tests/
