
##[Portuguese Readme](../../README.md) // [English Readme](./README.md)

# Facebook Scraper 

[![Build Status](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper.svg?branch=master)](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d78fb4221b49847ca9c/maintainability)](https://codeclimate.com/github/unb-cic-esw/facebook-page-post-scraper/maintainability)

## Making it Run

Once you have installed python3 and Git, cloned our repository and is using
a coding text editor (Atom, VSCode, Sublime ou Pycharm), follow these instructions.

Create an virtual environment and use-it

```
python3 -m venv venv
source venv/bin/activate
```

For those using Linux or MacOS
```
make install
```

For Windows
```
pip install -r requirements.txt
```

Once you have installed everything, is necessary ChromeDriver to update and configure the token. You
need to Download it and add to your PATH.
For Linux and MacOS users use:
```
make chromedriver
```
For Windows, is necessary to follow Splinter instructions:([Instruncions to download ChromeDriver](https://splinter.readthedocs.io/en/latest/drivers/chrome.html)).
Once ChromeDriver installed sucessfully use
```
make
```
and follow the instructions to use the program.

## Testing the code

For using the tests we wrote to check code functionalities

```
make
```
## verifying style

To check your code identation:

```
make style
```
Important to use it if wanting to send us a Pull Request :)

