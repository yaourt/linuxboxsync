__author__ = 'yaourt'

from ConfigManager import ConfigManager
from Indicator import Indicator
from gi.repository import Gtk

configmanager = ConfigManager()
configmanager.__access_token = None
indicator = Indicator(configmanager)
Gtk.main()
