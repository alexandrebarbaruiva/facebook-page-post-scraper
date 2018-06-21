"""
@token_manager Responsavel por lidar com tudo referente ao token.

Tudo relacionado ao token, desde pegar do arquivo, atualiza-lo e
salvar no arquivo novamente é definido aqui.
"""

import os
import sys
from configparser import ConfigParser
from getpass import getpass
from time import sleep
from splinter import Browser
from cryptography.fernet import Fernet
from scraper.page_scraper import Scraper
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)


path = str(os.getcwd()) + '/scraper/'


def retrieve_token_file(file='config.ini'):
    """Recebe token do arquivo config.ini."""
    try:
        config = ConfigParser()
        config.read_file(open(path + file))
        if ('DEFAULT' in config.keys()):
            if ('token' in config['DEFAULT'].keys()):
                return(config['DEFAULT']['token'])
        return 'Token with bad structure'
    except Exception:
        return False


def retrieve_password_file(file='config.ini'):
    """Recupera usuario e senha do arquivo config.ini."""
    try:
        config = ConfigParser()
        config.read_file(open(path + file))
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
    except Exception:
        return False


def update_token_file(file='config.ini', **kwargs):
    """Atualiza o token no arquivo config.ini."""
    config = ConfigParser()
    config.read(path + file)

    if len(kwargs.keys()) > 0:
        # Se kwargs tem todas as informaçoes para a senha.
        if {'user', 'password', 'utoken'} == set(kwargs):
            config['USER'] = kwargs
            with open(path + file, 'w') as configfile:
                config.write(configfile)
            return 'User and password updated.'

        # Se kwargs tem infromações para o token.
        if ('token' in kwargs.keys()):
            config['DEFAULT'] = {'token': kwargs['token']}
            with open(path + file, 'w') as configfile:
                config.write(configfile)
            print('\x1b[04;01;32mNew token written successfuly.\x1b[0m\n')
            return 'New token written successfuly.'
    print('\x1b[04;01;31mFile not updated.\x1b[0m')
    return 'File not updated.'


def generate_token_file(new_token=None, file='config.ini'):
    """
    Gera um arquivo config.ini vazio caso não exista.

    Caso exista, retona vazio.
    """
    if(not retrieve_token_file(file)):
        token_data = '[DEFAULT]\ntoken = \'' + str(new_token) + '\''
        with open(path + file, 'w') as token_file:
            token_file.write(token_data)
            return [True, new_token]
    else:
        return [False, 'File already exists']


def collect_token_automatically(email, password, file='config.ini'):
    """
    Loga no Facebook e atualiza o token.

    Quando o usuario aceitar os termos do Facebook, essa função
    logará no Facebook do usuário, pegará o token e salvará
    no arquivo config.ini.
    """
    executable_path = {'executable_path': os.environ.get('GOOGLE_CHROME_SHIM')}
    with Browser('chrome', headless=True, **executable_path) as browser:
        # Visita o site de desenvolvedores do Facebook.
        try:
            browser.driver.set_window_size(1100, 800)
            url = "https://developers.facebook.com/tools/explorer" \
                "/?locale=en_US"
            browser.visit(url)
            # Procura o butão de login, caso nao encontre resulta em erro.
            # Coneta no facebook.
            browser.click_link_by_partial_href('login')
        except Exception:
            print("\x1b[04;01;31mCouldn't open Facebook Dev site\x1b[0m")
            return 'Wasn`t possible to reach Facebook site. Are you online?'
        # Clica no butão de login.
        browser_login = browser.find_by_name('login')
        # Loga com o email e senha do usuario.
        try:
            browser.fill('email', email)
            browser.fill('pass', password)
            browser_login.click()
        # Requer a atualização do token.
            browser_access = browser.find_by_text('Get Token')
            browser_access.click()
        except Exception:
            print("\x1b[04;01;31m" + "Wrong User Login" + '\x1b[0m')
            return 'Wrong Facebook user or password'
        browser_accessus = browser.find_by_text(
            'Get User Access Token')
        browser_accessus.click()
        browser_token = browser.find_by_text('Get Access Token')
        browser_token.click()
        # Acha e pega o novo token.
        browser_token = browser.find_by_css(
            'label[class="_2toh _36wp _55r1 _58ak"]')
        browser_token = browser_token.first.html
        browser_token = browser_token.split("value", 1)[1]
        browser_token = browser_token.split("\"", 1)[1]
        browser_token = browser_token.split("\"", 1)[0]
        # atualiza o token no config.ini.
        if Scraper(browser_token).check_valid_token():
            update_token_file(file, **{'token': browser_token})
        else:
            print('Token not valid')
        browser.quit()
    return Scraper(browser_token)


def check_automatic_collection(file='config.ini'):
    """
    Recupera o token automaticamente.

    A partir do momento que config.ini tem o email e
    senha do usuario, atualiza automaticamente o token.
    """
    try:
        # Tenta pegar o token.
        email, password = get_user_password_decrypted(file)
        token_is_valid = collect_token_automatically(email, password)
        if(token_is_valid.check_valid_token()):
            print("\x1b[04;01;32mSet Token Is Valid\x1b[0m\n")
            print("\x1b[04;01;32mAuto Token function Completed\x1b[0m")
            return True
        print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
        return False
    except Exception:
        # something went wrong getting the token
        print("\x1b[04;01;31mAuto Token function Failed!\x1b[0m")
        return 'Wrong user or password.'


def check_semi_automatic_collection(file='config.ini',
                                    email=None,
                                    password=None):
    """
    Coleta o token mas necessita do input do usuario.

    Maior parte da coleta é automatica, mas necessita
    do email e senha do usuario como input.
    """
    os.system("clear")
    print('Email from your Facebook Account:')
    if email is None:
        email = input()
    if password is None:
        password = getpass()
    update_token_file(file, **encrypt_user_password(email, password))
    try:
        # tTenta pegar o token.
        token_is_valid = collect_token_automatically(email, password)
        if(token_is_valid.check_valid_token()):
            print("\x1b[04;01;32mSet Token Is Valid\x1b[0m\n")
        else:
            print("\x1b[04;01;31mSet Token is not Valid\x1b[0m\n")
        print("\x1b[04;01;32mAuto Token function Completed\x1b[0m")
        return True
    except Exception:
        # Alguma coisa deu errado na coleta.
        print("\x1b[04;01;31mAuto Token function Failed!\x1b[0m")
        return False


def collect_token(file='config.ini'):
    """
    Coleta token manualmente para quem é a primeira vez.

    Ou automaticamente caso o usuario ja tenha o feito.
    """
    os.system("clear")

    if retrieve_password_file(file):
        return check_automatic_collection(file)
    else:
        return check_semi_automatic_collection(file)


def encrypt_user_password(user, password):
    """Encripta o email e a senha e salva no config.ini."""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    user_byte = str.encode(user)
    pass_byte = str.encode(password)
    encrypted_user = cipher_suite.encrypt(user_byte)
    encrypted_pass = cipher_suite.encrypt(pass_byte)
    return({'user': encrypted_user, 'password': encrypted_pass, 'utoken': key})


def decrypt_user_password(**kwargs):
    """Descriptografa o email e senha do config.ini para um dado token."""
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
    """Descriptografa o usuario e senha do config.ini."""
    try:
        return decrypt_user_password(**retrieve_password_file(file))
    except Exception as inst:
        print("Token file not found.", inst)
        return False


if __name__ == '__main__':
    collect_token()
