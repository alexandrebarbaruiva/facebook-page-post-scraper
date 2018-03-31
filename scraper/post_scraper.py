import facebook
import requests
import os
import sys
from configparser import ConfigParser
import logging


def retrieve_token():
    """
    Retrives token from config.ini file on scraper folder
    """
    try:
        config = ConfigParser()
        config.read_file(open(str(os.getcwd())+'/scraper/config.ini'))
        return(config['DEFAULT']['token'])
    except e:
        return(e)

class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 404

    def check_status_code(self):
        return self.status_code
