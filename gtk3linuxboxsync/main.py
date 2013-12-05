__author__ = 'yaourt'

import os
import ConfigParser
from datetime import datetime
from gi.repository import GLib,Gtk
from OAuthGUI import OAuthGUI

# OAuth token info
access_token = None
access_key_validity = None
refresh_token = None
refresh_token_validity = None

confDir = os.path.join(GLib.get_user_config_dir(), 'ulinuxboxsync')
confFile = os.path.join(confDir, "config.ini")
config = ConfigParser.ConfigParser()

if os.path.isfile(confFile):
    config.read(confFile)
    access_token = config.get('OAuth', 'access_token')
    access_key_validity = config.get('OAuth', 'access_token_validity')
    refresh_token = config.get('OAuth', 'refresh_token')
    refresh_token_validity = config.get('OAuth', 'refresh_token_validity')
else:
    if not os.path.exists(confDir):
        os.makedirs(confDir)
        config.add_section('OAuth')
        config.set('OAuth', 'access_token', 'None')
        config.set('OAuth', 'access_token_validity', 'None')
        config.set('OAuth', 'refresh_token', 'None')
        config.set('OAuth', 'refresh_token_validity', 'None')
        with open(confFile, 'wb') as confFile:
            config.write(confFile)
if(access_token is None and refresh_token is None):
    oauth_gui = OAuthGUI(config, confFile)
    Gtk.main()

now = datetime.utcnow()
if(access_token is not None):
    oauth_gui = OAuthGUI(config, confFile)
    Gtk.main()
