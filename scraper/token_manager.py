import os
from configparser import ConfigParser
import webbrowser
from time import sleep
from splinter import Browser
from time import sleep
from getpass import getpass

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
    with Browser('chrome') as browser:
        # Visit URL
        url = "https://developers.facebook.com/tools/explorer/"
        browser.visit(url)
        # Find and click the 'search' button
        browser.click_link_by_partial_href('login')
        Blogin = browser.find_by_name('login')
        # Interact with elements
        browser.fill('email', email)
        browser.fill('pass', password)
        Blogin.click()
        Baccess = browser.find_by_text('Obter token')
        Baccess.click()
        Baccessus = browser.find_by_text('Obter token de acesso do usuário')
        Baccessus.click()
        Btoken = browser.find_by_text('Obter token de acesso')
        Btoken.click()
        Token = browser.find_by_css('label[class="_2toh _36wp _55r1 _58ak"]')
        Token = Token.first.html
        Token = Token.split("value", 1)[1]
        Token = Token.split("\"", 1)[1]
        Token = Token.split("\"", 1)[0]
        update_token(Token)
        print("Auto Token function Completed")
        browser.quit()


if __name__ == '__main__':
    cond = "something"
    while (cond != "Y" and cond != "N"):
        print(
            "\nIs it your first time getting User Access Token?" +
            "\nType \"Y\" OR \"N\"")
        cond = input().upper()
    if(cond == "N"):
        print('Email from your Facebook Account:')
        email = input()
        password = getpass()
        auto(email, password)

    elif(cond == "Y"):
        print(
            "\n1. Click on \"Get token\" then \"Get User Access Token\"." +
            "\n2. Then select \"manage_pages\",\"publish_pages\"," +
            "\n\"pages_show_list\" and \"pages_manage_instant_articles\"." +
            "\n3. Finish by clicking on \"Get Access Token\"." +
            "\n\nNow paste your user Access Token here:"
        )
        sleep(5.0)
        webbrowser.open('https://developers.facebook.com/tools/explorer')
        sleep(2.0)
        token = input()
        update_token(token)
