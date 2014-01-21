__author__ = 'yaourt'

from gtk3linuxboxsync.ConfigManager import ConfigManager
import logging

logger = logging.getLogger('ulinuxsync.ConfigManager.test')
config_manager = ConfigManager()
token = config_manager.access_token
logger.debug('Access token: %s', token)
