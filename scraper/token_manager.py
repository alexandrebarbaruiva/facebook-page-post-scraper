import os
import sys
from configparser import ConfigParser
import webbrowser
from splinter import Browser
from time import sleep
from cryptography.fernet import Fernet
from getpass import getpass
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from scraper.post_scraper import Scraper

path = str(os.getcwd())+'/scraper/'


def retrieve_token_file(file='config.ini'):
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
    except Exception as inst:
        return False


def retrieve_password_file(file='config.ini'):
    """
    Retrieves user and password from config.ini file on scraper folder
    """
    try:
        config = ConfigParser()
        config.read_file(open(path+file))
        if ('DEFAULT' in config.keys()):
            if ('token' in config['DEFAULT'].keys()):
                return(
                    [
                        config['DEFAULT']['user'],
                        config['DEFAULT']['password'],
                        config['DEFAULT']['utoken']
                    ]
                )
        return 'Token with bad user/password structure'
    except Exception as inst:
        return False


def update_token_file(new_token=None, file='config.ini'):
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
    if(not retrieve_token_file(file)):
        token_data = '[DEFAULT]\ntoken = \'' + str(new_token) + '\''
        with open(path+file, 'w') as token_file:
            token_file.write(token_data)
            return [True, new_token]
    else:
        return [False, 'File already exists']


def collect_token(email, password):
    """
    Case User already had accepted Facebook Terms and Conditions,
    this function will login on user's Facebook and get his
    "User Token Acces" and save in config.ini
    """
    with Browser('chrome') as browser:
        # Visit Facebook developers web site
        try:
            url = "https://developers.facebook.com/tools/explorer/"
            browser.visit(url)
            # Find the login button, if not found means error
            # conecting with the Facebook
            browser.click_link_by_partial_href('login')
        except Exception as inst:
            print("\x1b[04;01;31mCouldn't open Facebook Dev site\x1b[0m")
            raise Exception
        # Click on login button
        browser_login = browser.find_by_name('login')
        print(browser_login)
        # Login with email and password from the user
        try:
            browser.fill('email', email)
            browser.fill('pass', password)
            browser_login.click()
        # Request the updated User access token
            browser_access = browser.find_by_text('Obter token')
            browser_access.click()
        except Exception as inst:
            print("\x1b[04;01;31m" + "Wrong User Login" + '\x1b[0m')
            raise Exception
        browser_accessus = browser.find_by_text(
            'Obter token de acesso do usuário'
        )
        browser_accessus.click()
        browser_token = browser.find_by_text('Obter token de acesso')
        browser_token.click()
        # find and catch the new user acces token
        browser_token = browser.find_by_css(
            'label[class="_2toh _36wp _55r1 _58ak"]'
        )
        browser_token = browser_token.first.html
        browser_token = browser_token.split("value", 1)[1]
        browser_token = browser_token.split("\"", 1)[1]
        browser_token = browser_token.split("\"", 1)[0]
        # update new token into config.ini and print if it worked
        update_token_file(browser_token)
        browser.quit()
    valid_token = Scraper(browser_token)
    return valid_token


def collect_token_manually():
    """
    Case is the first time the User try to get the Token, User
    will have to accept Facebook Terms and Conditions,
    this function will open facebook page so he can login on user's Facebook,
    get his "User Token Acces", paste on the terminal so we save in config.ini
    """
    sleep(5.0)
    webbrowser.open('https://developers.facebook.com/tools/explorer')
    sleep(2.0)
    # update token and print if it worked
    manually_get_token = input()
    update_token_file(manually_get_token)
    # checks if the User has pasted correctly the user acces token
    token_is_valid = Scraper(manually_get_token)
    return token_is_valid


def automate_token_collection():
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
            token_is_valid = collect_token(email, password)
            if(token_is_valid.check_valid_token()):
                print("\x1b[04;01;32m" + "Set Token Is Valid" + '\x1b[0m\n')
            else:
                print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
            print("\x1b[04;01;32m"+"Auto Token function Completed"+"\x1b[0m")
        except Exception as inst:
            # something went wrong getting the token
            print("\x1b[04;01;31m"+"Auto Token function Failed!"+"\x1b[0m")

    elif(cond == "Y"):
        os.system("clear")
        print(
            "1. Login on your Facebook Account" +
            "\n2. Click on \"Get token\" then \"Get User Access Token\"." +
            "\n3. Then select \"manage_pages\",\"publish_pages\"," +
            "\n\"pages_show_list\" and \"pages_manage_instant_articles\"." +
            "\n4. Finish by clicking on \"Get Access Token\"." +
            "\n\nNow paste your user Access Token here:"
        )  # wait enough time so the user can read the menu
        token_is_valid = collect_token_manually()
        if(token_is_valid.check_valid_token()):
            print("\x1b[04;01;32m" + "Set Token Is Valid" + '\x1b[0m\n')
        else:
            print("\x1b[04;01;31m" + "Set Token is not Valid" + '\x1b[0m\n')
        print("\x1b[04;01;32m" + "Auto Token function Completed" + '\x1b[0m')
        sleep(2.0)


def encrypt_user_password(user, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    user_byte = str.encode(user)
    pass_byte = str.encode(password)
    encrypted_user = cipher_suite.encrypt(user_byte)
    encrypted_pass = cipher_suite.encrypt(pass_byte)
    return([encrypted_user, encrypted_pass, key])


if __name__ == '__main__':
    automate_token_collection()
