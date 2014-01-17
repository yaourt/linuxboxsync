__author__ = 'yaourt'

import json
from datetime import datetime, timedelta
from gi.repository import GLib, Gtk
import os
import ConfigParser
import logging
import urllib2

class ConfigManager:
    __validity_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self.__logger = logging.getLogger('ulinuxsync.ConfigManager')
        self.__conf_dir = os.path.join(GLib.get_user_config_dir(), 'ulinuxboxsync')
        self.__conf_file = os.path.join(self.__conf_dir, "config.ini")
        self.__config = ConfigParser.ConfigParser()

        if os.path.isfile(self.__conf_file):
            self.__config.read(self.__conf_file)
            self.__access_token = self.__config.get('OAuth', 'access_token')
            if self.__access_token != 'None':
                self.__access_token_validity =\
                    datetime.strptime(self.__config.get('OAuth', 'access_token_validity'), ConfigManager.__validity_format)
            else:
                self.__access_token = None
                self.__access_token_validity = None

            self.__refresh_token = self.__config.get('OAuth', 'refresh_token')
            if self.__refresh_token != 'None':
                self.__refresh_token_validity =\
                    datetime.strptime(self.__config.get('OAuth', 'refresh_token_validity'), ConfigManager.__validity_format)
            else:
                self.__refresh_token = None
                self.__refresh_token_validity = None

        else:
            if not os.path.exists(self.__conf_dir):
                os.makedirs(self.__conf_dir)
            self.logout()


    def _update_from_json(self, json_string):
        json_object = json.loads(json_string)

        self.__config.set('OAuth', 'access_token', json_object['access_token'])
        self.__config.set('OAuth', 'access_token_validity', (datetime.utcnow() + timedelta(seconds=(json_object['expires_in'] - 120))).strftime(ConfigManager.__validity_format))
        self.__config.set('OAuth', 'refresh_token', json_object['refresh_token'])
        self.__config.set('OAuth', 'refresh_token_validity', (datetime.utcnow() + timedelta(days=59)).strftime(ConfigManager.__validity_format))
        with open(self.__conf_file, 'wb') as configFile:
            self.__config.write(configFile)
        self.__access_token = self.__config.get('OAuth', 'access_token')
        self.__access_token_validity = datetime.strptime(self.__config.get('OAuth', 'access_token_validity'), ConfigManager.__validity_format)
        self.__refresh_token = self.__config.get('OAuth', 'refresh_token')
        self.__refresh_token_validity = datetime.strptime(self.__config.get('OAuth', 'refresh_token_validity'), ConfigManager.__validity_format)

    @property
    def access_token(self):
        if self.__access_token is not None and \
           self.__access_token_validity is not None and \
           self.__access_token_validity < datetime.utcnow():
                self.__logger.debug('Access token is expired, need to refresh it')
                return self._refresh_token()
        else:
            return self.__access_token

    def _refresh_token(self):
        if self.__refresh_token is not None and \
           self.__refresh_token_validity is not None and \
           self.__refresh_token_validity < datetime.utcnow():
            self.__logger.debug('Refresh token is expired. Full OAuth dance should be performed again')
            return None

        url = "https://linuxboxsyncbridge.appspot.com/refresh"

        params = {
            'refresh_token': self.__refresh_token,
        }

        data = json.dumps(params)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = None
        if 200 == f.getcode():
            response = f.read()
        f.close()

        if response is not None:
            self._update_from_json(response)
            return self.__access_token

    def logout(self):
        if not self.__config.has_section('OAuth'):
            self.__config.add_section('OAuth')
        self.__config.set('OAuth', 'access_token', 'None')
        self.__config.set('OAuth', 'access_token_validity', 'None')
        self.__config.set('OAuth', 'refresh_token', 'None')
        self.__config.set('OAuth', 'refresh_token_validity', 'None')
        with open(self.__conf_file, 'wb') as confFile:
            self.__config.write(confFile)

        self.__access_token = None
        self.__access_token_validity = None
        self.__refresh_token = None
        self.__refresh_token_validity = None
