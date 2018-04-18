import os
import sys
from configparser import ConfigParser
import webbrowser
from time import sleep
from splinter import Browser
from time import sleep
from getpass import getpass
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from scraper.post_scraper import Scraper

path = str(os.getcwd())+'/scraper/'


def retrieve_token(file='config.ini'):
    """
    Retrieves token from config.ini file on scraper folder
    """
    try:
        config = ConfigParser()
        config.read_file(open(path+file))
        if ('DEFAULT' in config.keys()):
            if ('token' in config['DEFAULT'].keys()):
                return(config['DEFAULT']['token'])
        return 'Token with bad structure'
    except:
        return False


def update_token(new_token=None, file='config.ini'):
    """
    Update token from config.ini file on scraper folder
    """
    if new_token is not None:
        config = ConfigParser()
        config['DEFAULT'] = {'token': new_token}
        with open(path+file, 'w') as configfile:
            config.write(configfile)
        return 'New token written successfuly.'
    else:
        return 'Token not updated.'


def generate_token_file(new_token=None, file='config.ini'):
    """
    Generate empty token file with token provided, else returns
    that token already exists
    """
    if(not retrieve_token(file)):
        token_data = '[DEFAULT]\ntoken = \'' + str(new_token) + '\''
        with open(path+file, 'w') as token_file:
            token_file.write(token_data)
            return [True, new_token]
    else:
        return [False, 'File already exists']


def auto(email, password):
    """
    Case User already had accepted Facebook Terms and Conditions,
    this function will login on user's Facebook and get his
    "User Token Acces" and save in config.ini
    """
    with Browser('chrome') as browser:
        # Visit Facebook developers web site
        url = "https://developers.facebook.com/tools/explorer/"
        browser.visit(url)
        # Find and click on login button
        browser.click_link_by_partial_href('login')
        Blogin = browser.find_by_name('login')
        # Login with email and password from the user
        try:
            browser.fill('email', email)
            browser.fill('pass', password)
            Blogin.click()
        # Request the updated User access token
            Baccess = browser.find_by_text('Obter token')
            Baccess.click()
        except Exception as inst:
            print("\x1b[04;01;31m" + "Wrong User Login" + '\x1b[0m')
        Baccessus = browser.find_by_text('Obter token de acesso do usuário')
        Baccessus.click()
        Btoken = browser.find_by_text('Obter token de acesso')
        Btoken.click()
        # find and catch the new user acces token
        Token = browser.find_by_css('label[class="_2toh _36wp _55r1 _58ak"]')
        Token = Token.first.html
        Token = Token.split("value", 1)[1]
        Token = Token.split("\"", 1)[1]
        Token = Token.split("\"", 1)[0]
        # update new token into config.ini and print if it worked
        update_token(Token)
        browser.quit()


if __name__ == '__main__':
    os.system("clear")
    cond = "something"
    while (cond != "Y" and cond != "N"):
        print(
            "Is it your first time getting User Access Token?" +
            "\nType \"Y\" OR \"N\"")
        cond = input().upper()
    if(cond == "N"):
        os.system("clear")
        print('Email from your Facebook Account:')
        email = input()
        password = getpass()
        try:
            # tried to get the token
            auto(email, password)
            print("\x1b[04;01;32m"+"Auto Token function Completed"+"\x1b[0m")
        except Exception as inst:
            # something went wrong getting the token
            print("\x1b[04;01;31m"+"Auto Token function Failed!"+"\x1b[0m")

    elif(cond == "Y"):
        os.system("clear")
        print(
            "1. Click on \"Get token\" then \"Get User Access Token\"." +
            "\n2. Then select \"manage_pages\",\"publish_pages\"," +
            "\n\"pages_show_list\" and \"pages_manage_instant_articles\"." +
            "\n3. Finish by clicking on \"Get Access Token\"." +
            "\n\nNow paste your user Access Token here:"
        )  # wait enough time so the user can read the menu
        sleep(5.0)
        webbrowser.open('https://developers.facebook.com/tools/explorer')
        sleep(2.0)
        # update token and print if it worked
        token = input()
        update_token(token)
        # checks if the User has pasted correctly the user acces token
        Token_is_valid = Scraper(token)
        if(Token_is_valid.check_valid_token()):
            print("\x1b[04;01;32m" + "Set Token Is Valid" + '\x1b[0m\n')
        else:
            print("\x1b[04;01;31m" + "Set Token is not Valid" + '\x1b[0m\n')
        print("\x1b[04;01;32m" + "Auto Token function Completed" + '\x1b[0m')
        sleep(3.0)
