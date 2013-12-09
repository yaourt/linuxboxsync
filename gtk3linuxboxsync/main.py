__author__ = 'yaourt'

from ConfigManager import ConfigManager
from Indicator import Indicator
from gi.repository import Gtk

configmanager = ConfigManager()
indicator = Indicator(configmanager)
Gtk.main()
