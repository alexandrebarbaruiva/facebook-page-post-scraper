import os
from configparser import ConfigParser
import webbrowser
from time import sleep

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
    except Exception as inst:
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


if __name__ == '__main__':
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
