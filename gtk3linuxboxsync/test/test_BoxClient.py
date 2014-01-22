__author__ = 'yaourt'

import logging
from gtk3linuxboxsync.ConfigManager import ConfigManager
from gtk3linuxboxsync.BoxClient import BoxClient

config_manager = ConfigManager()
client = BoxClient(config_manager)
client.listRootFolder()
