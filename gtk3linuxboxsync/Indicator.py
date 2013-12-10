from gtk3linuxboxsync.OAuthGUI import OAuthGUI

__author__ = 'yaourt'

import os
from gi.repository import Gtk

try:
    from gi.repository import AppIndicator3  # @UnresolvedImport
    HAS_INDICATOR = True
except:
    HAS_INDICATOR = False

class Indicator(object):


    def __init__(self, configmanager):
        self.configmanager = configmanager
        _cur_dir = os.path.dirname(__file__)
        self.ind = AppIndicator3.Indicator.new(
                        "LinuxBoxSync (unofficial)",
                        "",
                        AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        iconpath = os.path.join(_cur_dir, 'b64.png')
        self.ind.set_icon(iconpath)
        iconpath_active = os.path.join(_cur_dir, 'b64-active.png')
        self.ind.set_attention_icon_full(iconpath_active, "/!\ WARNING")

        # Menu
        # self.menu = Gtk.Menu()
        self.menu = self.buildMenu()
        # self.menu = self.buildMenu2()
        # self.menu = self.buildMenu3()
        self.ind.set_menu(self.menu)
        # self.buildMenu()

        #self.login()

    def set_label(self, txt):
        self.ind.set_label(txt, txt)

    def set_attention(self, attention):
        if attention:
            self.ind.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
            #self.ind.set_label("Attention Label 01234567890123456789012345678901234567890123456789012345678901234567890123456789", "")
        else:
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            #self.ind.set_label("", "")

    def swap_attention(self, item):
        self.set_attention(item.get_active())

    def quit(self, item):
        Gtk.main_quit()

    def login(self):
        access_token = self.configmanager.get_access_token()
        if access_token is None:
            oauthgui = OAuthGUI(self.configmanager)

    def buildMenu(self):
        menu = Gtk.Menu()

        connect_group = []
        self.connect_item = Gtk.RadioMenuItem.new_with_mnemonic(connect_group, '_Connect')
        connect_group = self.connect_item.get_group()
        self.connect_item.show()
        self.connect_item.connect('activate', self.swap_attention)
        menu.append(self.connect_item)

        self.disconnect_item = Gtk.RadioMenuItem.new_with_mnemonic(connect_group, '_Disconnect')
        connect_group = self.disconnect_item.get_group()
        self.disconnect_item.show()
        self.disconnect_item.connect('activate', self.swap_attention)
        menu.append(self.disconnect_item)

        separator1 = Gtk.SeparatorMenuItem()
        separator1.show()
        menu.append(separator1)

        login_group = []
        self.login_item = Gtk.RadioMenuItem.new_with_mnemonic(login_group, '_Login')
        login_group = self.login_item.get_group()
        self.login_item.show()
        menu.append(self.login_item)
        self.logout_item = Gtk.RadioMenuItem.new_with_mnemonic(login_group, 'Log_out')
        login_group = self.logout_item.get_group()
        self.logout_item.show()
        menu.append(self.logout_item)

        separator1 = Gtk.SeparatorMenuItem()
        separator1.show()
        menu.append(separator1)

        self.quit_item = Gtk.MenuItem.new_with_mnemonic('_Quit')
        self.quit_item.show()
        self.quit_item.connect('activate', self.quit)
        menu.append(self.quit_item)

        return menu
