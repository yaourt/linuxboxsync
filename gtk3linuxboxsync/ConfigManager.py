__author__ = 'yaourt'

import json
from datetime import datetime, timedelta
from gi.repository import GLib, Gtk
import os
import ConfigParser
import logging
import urllib2

class ConfigManager:
    _validity_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self.logger = logging.getLogger('ulinuxsync.ConfigManager')
        self.conf_dir = os.path.join(GLib.get_user_config_dir(), 'ulinuxboxsync')
        self.conf_file = os.path.join(self.conf_dir, "config.ini")
        self.config = ConfigParser.ConfigParser()

        if os.path.isfile(self.conf_file):
            self.config.read(self.conf_file)
            self.access_token = self.config.get('OAuth', 'access_token')
            if self.access_token != 'None':
                self.access_token_validity =\
                    datetime.strptime(self.config.get('OAuth', 'access_token_validity'), ConfigManager._validity_format)
            else:
                self.access_token = None
                self.access_token_validity = None

            self.refresh_token = self.config.get('OAuth', 'refresh_token')
            if self.refresh_token != 'None':
                self.refresh_token_validity =\
                    datetime.strptime(self.config.get('OAuth', 'refresh_token_validity'), ConfigManager._validity_format)
            else:
                self.refresh_token = None
                self.refresh_token_validity = None

        else:
            if not os.path.exists(self.conf_dir):
                os.makedirs(self.conf_dir)

            self.config.add_section('OAuth')
            self.config.set('OAuth', 'access_token', 'None')
            self.config.set('OAuth', 'access_token_validity', 'None')
            self.config.set('OAuth', 'refresh_token', 'None')
            self.config.set('OAuth', 'refresh_token_validity', 'None')
            with open(self.conf_file, 'wb') as confFile:
                self.config.write(confFile)

            self.access_token = None
            self.access_token_validity = None
            self.refresh_token = None
            self.refresh_token_validity = None

    def update_from_json(self, json_string):
        json_object = json.loads(json_string)

        self.config.set('OAuth', 'access_token', json_object['access_token'])
        self.config.set('OAuth', 'access_token_validity', (datetime.utcnow() + timedelta(seconds=(json_object['expires_in'] - 120))).strftime(ConfigManager._validity_format))
        self.config.set('OAuth', 'refresh_token', json_object['refresh_token'])
        self.config.set('OAuth', 'refresh_token_validity', (datetime.utcnow() + timedelta(days=59)).strftime(ConfigManager._validity_format))
        with open(self.conf_file, 'wb') as configFile:
            self.config.write(configFile)
        self.access_token = self.config.get('OAuth', 'access_token')
        self.access_token_validity = datetime.strptime(self.config.get('OAuth', 'access_token_validity'), ConfigManager._validity_format)
        self.refresh_token = self.config.get('OAuth', 'refresh_token')
        self.refresh_token_validity = datetime.strptime(self.config.get('OAuth', 'refresh_token_validity'), ConfigManager._validity_format)

    def get_access_token(self):
        if self.access_token is not None and \
           self.access_token_validity is not None and \
           self.access_token_validity < datetime.utcnow():
                self.logger.debug('Access token is expired, need to refresh it')
                return self._refresh_token()
        else:
            return self.access_token

    def _refresh_token(self):
        if self.refresh_token is not None and \
           self.refresh_token_validity is not None and \
           self.refresh_token_validity < datetime.utcnow():
            self.logger.debug('Refresh token is expired. Full OAuth dance should be performed again')
            return None

        url = "https://linuxboxsyncbridge.appspot.com/refresh"

        params = {
            'refresh_token': self.refresh_token,
        }

        data = json.dumps(params)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = None
        if 200 == f.getcode():
            response = f.read()
        f.close()

        if response is not None:
            self.update_from_json(response)
            return self.access_token