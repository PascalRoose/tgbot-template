import os
from configparser import ConfigParser
from secrets import token_urlsafe

from appdirs import AppDirs

_path = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(_path))

NAME = os.path.basename(_root)
DIRS = AppDirs(appname=NAME, appauthor='TelegramBots')

MEMKEY = token_urlsafe(8)


class Settings(object):
    class Webhook(object):
        def __init__(self, webhook: dict):
            self.ENABLED = True if webhook['Enabled'] == 'true' else False
            self.IP = webhook['IP']
            self.PORT = int(webhook['Port'])
            self.PATH = webhook['Path']
            self.URL = webhook['URL']

    def __init__(self, config: dict):
        self.TOKEN = config['DEFAULT']['Token']
        self.ADMIN = int(config['DEFAULT']['Admin'])

        self.WEBHOOK = Settings.Webhook(config['Webhook'])


_conf = ConfigParser()
_settings_path = os.path.join(DIRS.user_config_dir, "settings.ini")

for path in [DIRS.user_cache_dir, DIRS.user_config_dir, DIRS.user_log_dir]:
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


if os.path.exists(_settings_path):
    _conf.read(_settings_path)

else:
    """Setup settings.ini"""
    print('Running configuration setup')

    _conf['DEFAULT']['Token'] = input('Bot token: ')
    _conf['DEFAULT']['Admin'] = '0'

    _conf.add_section('Webhook')
    enable_webhook = input('Do you want to enable updates over webhook? [y/N] ')

    if enable_webhook == 'y' or enable_webhook == 'Y':
        _conf['Webhook']['Enabled'] = 'true'
        _conf['Webhook']['IP'] = input('Listen IP: ')
        _conf['Webhook']['Port'] = input('Port number: ')
        _conf['Webhook']['Path'] = input('Path: ')
        _conf['Webhook']['URL'] = input('URL: ')
    else:
        _conf['Webhook']['Enabled'] = 'false'
        _conf['Webhook']['IP'] = '0.0.0.0'
        _conf['Webhook']['Port'] = '443'
        _conf['Webhook']['Path'] = _conf['DEFAULT']['Token']
        _conf['Webhook']['URL'] = f"https://example.com:{_conf['Webhook']['Port']}/{_conf['Webhook']['Path']}"

    with open(_settings_path, 'w+') as _settings_file:
        _conf.write(_settings_file)

settings = Settings(_conf)


def set_admin(tgid: int):
    settings.ADMIN = tgid
    _conf['DEFAULT']['Admin'] = str(tgid)

    with open(_settings_path, 'w+') as _settings_file:
        _conf.write(_settings_file)
