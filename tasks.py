from invoke import task


# BASICS #
@task()
def run(c):
    """
    Collects all pages in entidades.csv
    """
    c.run('python3 -m scraper.collector')


@task
def autotoken(c):
    """
    Open Facebook Developers web page so that the user can
    take a new token and update config.ini file
    """
    c.run('python3 -m scraper.token_manager')


@task
def createconfig(c):
    """
    Creates config.ini in scraper dir with the expected way
    to use it
    """
    c.run('echo "[DEFAULT]\ntoken = YOURTOKENHERE" >./scraper/config.ini')


@task
def chromedriver(c):
    """
    Install chromedriver on Linux to get the token automatically
    """
    print('Use make chromedriver for now!')

@task
def clean(c):
    """
    Removes all json files
    """
    c.run('rm -rf ./json')
    c.run('rm -rf ./htmlcov')
    c.run('rm -rf ./.coverage')
    c.run('rm -rf ./json/')



# TESTING #
@task(clean)
def test(c):
    """
    Runs the tests using green3
    """
    c.run('green3 -vv')


@task(pre=clean)
def cov(c):
    """
    Checks test coverage for the code
    """
    c.run('coverage run -m py.test tests/test_page_scraper.py tests/test_token_manager.py')
    c.run('coverage report -m scraper/page_scraper.py scraper/token_manager.py')
    c.run('coverage html scraper/page_scraper.py scraper/token_manager.py')


@task
def style(c):
    """
    Checks if your code is following PEP8
    """
    c.run('pycodestyle tests/. scraper/. server/. --ignore=E402,W504,E127')


# @task(pre=[style, clean])
# def full(c):
#     """
#     Runs tests, checks code coverage and PEP8
#     """
#     c.run('python3 -m scraper.collector')


@task(pre=[style, clean])
def travis(c):
    """
    What runs on Travis CI
    """
    c.run('green3 tests/test_page_scraper_unit.py -vv -f')
