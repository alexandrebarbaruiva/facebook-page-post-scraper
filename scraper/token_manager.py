import os
import sys
from configparser import ConfigParser
import webbrowser
from getpass import getpass
from time import sleep
from splinter import Browser
from cryptography.fernet import Fernet
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from page_scraper import Scraper

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
        if ('USER' in config.keys()):
            if {'user', 'password', 'utoken'} <= set(config['USER']):
                return(
                    {
                        'user': config['USER']['user'],
                        'password': config['USER']['password'],
                        'utoken': config['USER']['utoken']
                    }
                )
        return False
    except Exception as inst:
        return False


def update_token_file(file='config.ini', **kwargs):
    """
    Update token from config.ini file on scraper folder
    """
    config = ConfigParser()
    config.read(path+file)

    if len(kwargs.keys()) > 0:
        # if kwargs has all info for password
        if {'user', 'password', 'utoken'} == set(kwargs):
            config['USER'] = kwargs
            with open(path+file, 'w') as configfile:
                config.write(configfile)
            return 'User and password updated.'

        # if kwargs has token info
        if ('token' in kwargs.keys()):
            config['DEFAULT'] = {'token': kwargs['token']}
            with open(path+file, 'w') as configfile:
                config.write(configfile)
            print('\x1b[04;01;32mNew token written successfuly.\x1b[0m\n')
            return 'New token written successfuly.'
    print('\x1b[04;01;31mFile not updated.\x1b[0m')
    return 'File not updated.'


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


def collect_token_automatically(email, password, file='config.ini'):
    """
    When user has already accepted Facebook Terms and Conditions,
    this function will login on user's Facebook and get his
    "User Token Acces" and save in config.ini
    """
    with Browser('chrome', headless=True) as browser:
        # Visit Facebook developers web site
        try:
            browser.driver.set_window_size(1100, 800)
            url = "https://developers.facebook.com/tools/explorer/"
            browser.visit(url)
            # Find the login button, if not found means error
            # conecting with the Facebook
            browser.click_link_by_partial_href('login')
        except Exception as inst:
            print("\x1b[04;01;31mCouldn't open Facebook Dev site\x1b[0m")
            return 'Não foi possível abrir o Facebook. Você está online?'
        # Click on login button
        browser_login = browser.find_by_name('login')
        # Login with email and password from the user
        try:
            browser.fill('email', email)
            browser.fill('pass', password)
            browser_login.click()
        # Request the updated User access token
            browser_access = browser.find_by_text('Obter token')
            browser_access.click()
        except Exception as inst:
            # try:
            #     os.remove(str(os.getcwd())+'/scraper/'+file)
            # except Exception as inst:
            #     pass
            print("\x1b[04;01;31m" + "Wrong User Login" + '\x1b[0m')
            return 'Wrong Facebook user or password'
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
        if Scraper(browser_token).check_valid_token():
            update_token_file(file, **{'token': browser_token})
        else:
            print('Token not valid')
        browser.quit()
    return Scraper(browser_token)


def collect_token_manually(file='config.ini'):
    """
    Case is the first time the User try to get the Token, User
    will have to accept Facebook Terms and Conditions,
    this function will open facebook page so he can login on user's Facebook,
    get his "User Token Acces", paste on the terminal so we save in config.ini
    """
    webbrowser.open('https://developers.facebook.com/tools/explorer')
    # update token and print if it worked
    manually_get_token = input()
    update_token_file(file, **{'token': manually_get_token})
    # checks if the User has pasted correctly the user acces token
    token_is_valid = Scraper(manually_get_token)
    return token_is_valid


def check_automatic_collection(file='config.ini'):
    try:
        # tried to get the token
        print(
            "\x1b[04;01;32m" +
            "Getting credentials and collecting token" +
            "\x1b[0m\n"
        )
        email, password = get_user_password_decrypted(file)
        token_is_valid = collect_token_automatically(email, password)
        if(token_is_valid.check_valid_token()):
            print("\x1b[04;01;32m" + "Set Token Is Valid" + '\x1b[0m\n')
            print("\x1b[04;01;32m"+"Auto Token function Completed"+"\x1b[0m")
            return True
        print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
        return False
    except Exception as inst:
        # something went wrong getting the token
        print("\x1b[04;01;31m"+"Auto Token function Failed!"+"\x1b[0m")
        return 'Wrong user or password.'


def check_semi_automatic_collection(
    file='config.ini', email=None, password=None
):
    os.system("clear")
    print('Email from your Facebook Account:')
    if email is None:
        email = input()
    if password is None:
        password = getpass()
    update_token_file(file, **encrypt_user_password(email, password))
    try:
        # tried to get the token
        token_is_valid = collect_token_automatically(email, password)
        if(token_is_valid.check_valid_token()):
            print(
                "\x1b[04;01;32m" +
                "Set Token Is Valid" +
                "\x1b[0m\n"
            )

        else:
            print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
        print(
            "\x1b[04;01;32m" +
            "Auto Token function Completed" +
            "\x1b[0m"
        )
        return True
    except Exception as inst:
        # something went wrong getting the token
        print("\x1b[04;01;31m"+"Auto Token function Failed!"+"\x1b[0m")
        return False


def check_manual_collection(file='config.ini'):
    os.system("clear")
    print(
        "1. Login on your Facebook Account" +
        "\n2. Click on \"Get token\" then \"Get User Access Token\"." +
        "\n3. Then select \"manage_pages\",\"publish_pages\",\n" +
        "\"pages_show_list\" and \"pages_manage_instant_articles\"." +
        "\n4. Finish by clicking on \"Get Access Token\"." +
        "\n\nNow paste your user Access Token here:"
    )
    sleep(3.0)
    token_is_valid = collect_token_manually(file)
    if token_is_valid.check_valid_token():
        print("\x1b[04;01;32mSet Token Is Valid\x1b[0m\n")
        print("\x1b[04;01;32mAuto Token function Completed\x1b[0m")
        sleep(1.0)
        return True
    print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
    print("\x1b[04;01;32mAuto Token function Completed\x1b[0m")
    sleep(1.0)
    return False


def collect_token(file='config.ini'):
    """
    Function for collecting token manually if it's the first time or
    automatically if user has done the process at least once.
    """
    os.system("clear")
    cond = "something"

    if retrieve_password_file(file):
        return check_automatic_collection(file)
    else:
        while (cond != "Y" and cond != "N"):
            print(
                "Is it your first time getting User Access Token?" +
                "\nType \"Y\" OR \"N\"")
            cond = input().upper()
        if(cond == "N"):
            return check_semi_automatic_collection(file)
        elif(cond == "Y"):
            return check_manual_collection()


def encrypt_user_password(user, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    user_byte = str.encode(user)
    pass_byte = str.encode(password)
    encrypted_user = cipher_suite.encrypt(user_byte)
    encrypted_pass = cipher_suite.encrypt(pass_byte)
    return({'user': encrypted_user, 'password': encrypted_pass, 'utoken': key})


def decrypt_user_password(**kwargs):
    if {'user', 'password', 'utoken'} <= set(kwargs):
        try:
            kwargs['utoken'] = kwargs['utoken'][2:-1].encode()
            kwargs['user'] = kwargs['user'][2:-1].encode()
            kwargs['password'] = kwargs['password'][2:-1].encode()
        except Exception as inst:
            print(inst)
        cipher_suite = Fernet((kwargs['utoken']))
        user_d = str(cipher_suite.decrypt(kwargs['user']), 'utf-8')
        pass_d = str(cipher_suite.decrypt(kwargs['password']), 'utf-8')
        return [user_d, pass_d]
    return False


def get_user_password_decrypted(file='config.ini'):
    try:
        return decrypt_user_password(**retrieve_password_file(file))
    except Exception as inst:
        print("Token file not found.", inst)
        return False


if __name__ == '__main__':
    collect_token()
