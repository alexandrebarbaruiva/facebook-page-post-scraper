# Facebook Scraper

[![Build Status](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper.svg?branch=master)](https://travis-ci.org/unb-cic-esw/facebook-page-post-scraper)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d78fb4221b49847ca9c/maintainability)](https://codeclimate.com/github/unb-cic-esw/facebook-page-post-scraper/maintainability)

[:brazil: Readme](../../../../README.md) | [:us: Readme](./README.md)

[:brazil: Documentação](../../../Docs/Portuguese/Doc.md) |
[:us: Documentation](../../../Docs/English/Doc.md)

## Table of Content

* [Begin](#facebook-scraper)
* [Table of Content](#table-of-content)
* [Making it Run](#making-it-run)
* [Testing the code](#testing-the-code)
* [Verifying style](#verifying-style)
* [A Project by](#a-project-by)

## Making it Run

Once you have installed python3 and Git, cloned our repository and is using
a coding text editor (Atom, VSCode, Sublime ou Pycharm), follow these instructions.

Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

Now you have to install all packages related to the project

For those using Linux or MacOS

```
make install
```

For Windows

```
pip install -r requirements.txt
```

Once you have installed everything, install ChromeDriver to update and
configure the token. You need to download it and add it to your PATH.
For Linux and MacOS (Mac might not be working anymore) users use:

```
make chromedriver
```

For Windows, follow Splinter instructions:
([Instructions to download ChromeDriver](https://splinter.readthedocs.io/en/latest/drivers/chrome.html)).
Once ChromeDriver installed sucessfully use

```
make run
```

and follow the instructions to use the program. The file `entidades.csv` define
which pages we are scrapping, so update it as you want.

## Testing the code

For using the tests we wrote to check code functionalities

```
make
```

WARNING: It'll print a bunch of stuff. As long as it returns an exit code 1,
it's all fine.

## Verifying style

To check your code indentation and PEP8 related:

```
make style
```

Important to use it if you want to send us a Pull Request :smile:

## A Project by

[![alt text][unb]](https://www.unb.br/)

[unb]:../../../Images/logo_unb.png

Universidade de Brasília

[![alt text][resocie]](https://www.resocie.org/)

[resocie]:../../../Images/resocie.jpg

Resocie : Repensando as Relações entre Sociedade e Estado
