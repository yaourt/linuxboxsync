__author__ = 'yaourt'

from gtk3linuxboxsync.OAuthGUI import OAuthGUI
from gtk3linuxboxsync.ConfigManager import ConfigManager
from gi.repository import Gtk

config_manager = ConfigManager()
gui = OAuthGUI(config_manager)
Gtk.main()
gui.start()
