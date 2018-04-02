default: test

test:
	green3 . -vvv

run:
	python3 scraper/post_scraper.py

install:
	pip3 install -r requirements.txt

style:
	pycodestyle scraper/ tests/

cov:
	coverage run -m py.test tests/test.py
	coverage report -m scraper/post_scraper.py
	coverage html scraper/post_scraper.py

full:
	make test
	make cov
	make style
