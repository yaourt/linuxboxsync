__author__ = 'yaourt'

import box
import logging
import httplib

class BoxClient(object):
    def __init__(self, configmanager):
        # Enable wire debugging
        httplib.HTTPConnection.debuglevel = 1

        self.__logger = logging.getLogger('ulinuxsync.BoxClient')
        self.__configmanager = configmanager
        token = self.__configmanager.access_token
        if None is token:
            self.__logger.debug('No valid access token available')
        else:
            self.__client = box.BoxClient(token)

    def listRootFolder(self):
        rootfolder = self.__client.get_folder()
        self.__logger.debug('Root folder: %s', rootfolder)