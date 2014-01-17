from gtk3linuxboxsync.OAuthGUI import OAuthGUI

__author__ = 'yaourt'

import logging
import os
from gi.repository import Gtk

try:
    from gi.repository import AppIndicator3  # @UnresolvedImport
    HAS_INDICATOR = True
except:
    HAS_INDICATOR = False

class Indicator(object):


    def __init__(self, configmanager):
        self.__logger = logging.getLogger('ulinuxsync.Indicator')
        self.__configmanager = configmanager
        cur_dir = os.path.dirname(__file__)
        self.__ind = AppIndicator3.Indicator.new(
                        "LinuxBoxSync (unofficial)",
                        "",
                        AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.__ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        iconpath = os.path.join(cur_dir, 'b64.png')
        self.__ind.set_icon(iconpath)
        iconpath_active = os.path.join(cur_dir, 'b64-active.png')
        self.__ind.set_attention_icon_full(iconpath_active, "/!\ WARNING")

        # Menu
        self.__menu = self.__buildMenu()
        self.__ind.set_menu(self.__menu)

        # Radio menu items initial states
        self.__menuItemInitialStates()

        # Connect actions to callback
        self.__connectActions()


    def __set_label(self, txt):
        self.__ind.__set_label(txt, txt)

    def __set_attention(self, attention):
        if attention:
            self.__ind.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
            #self.ind.set_label("Attention Label 01234567890123456789012345678901234567890123456789012345678901234567890123456789", "")
        else:
            self.__ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            #self.ind.set_label("", "")

    def __swap_attention(self, item):
        self.__set_attention(item.get_active())

    def __buildMenu(self):
        menu = Gtk.Menu()

        self.__login_item = Gtk.ImageMenuItem.new_with_mnemonic('Logged _In')
        img = Gtk.Image()
        img.set_from_file(os.path.join(os.path.dirname(__file__), 'offline.png'))
        self.__login_item.set_image(img)
        self.__login_item.set_always_show_image(True)
        self.__login_item.show()
        menu.append(self.__login_item)

        # connect_group = []
        # self.__connect_item = Gtk.RadioMenuItem.new_with_mnemonic(connect_group, '_Connected')
        # connect_group = self.__connect_item.get_group()
        # self.__connect_item.show()
        # menu.append(self.__connect_item)
        #
        # self.__disconnect_item = Gtk.RadioMenuItem.new_with_mnemonic(connect_group, '_Disconnected')
        # connect_group = self.__disconnect_item.get_group()
        # self.__disconnect_item.show()
        # menu.append(self.__disconnect_item)
        #
        # separator1 = Gtk.SeparatorMenuItem()
        # separator1.show()
        # menu.append(separator1)
        #
        # login_group = []
        # self.__login_item = Gtk.RadioMenuItem.new_with_mnemonic(login_group, 'Logged _In')
        # login_group = self.__login_item.get_group()
        # self.__login_item.show()
        # menu.append(self.__login_item)
        # self.__logout_item = Gtk.RadioMenuItem.new_with_mnemonic(login_group, 'Logged _Out')
        # login_group = self.__logout_item.get_group()
        # self.__logout_item.show()
        # menu.append(self.__logout_item)

        separator1 = Gtk.SeparatorMenuItem()
        separator1.show()
        menu.append(separator1)

        # self.autoconn_item = Gtk.CheckMenuItem.new_with_mnemonic('_Auto connect')
        # self.autoconn_item.show()
        # menu.append(self.autoconn_item)
        #
        # separator2 = Gtk.SeparatorMenuItem()
        # separator2.show()
        # menu.append(separator2)

        # self.__about_item = Gtk.MenuItem.new_with_mnemonic('_About')
        # self.__about_item.show()
        # menu.append(self.__about_item)

        self.__quit_item = Gtk.MenuItem.new_with_mnemonic('_Quit')
        self.__quit_item.show()
        menu.append(self.__quit_item)

        return menu

    def __menuItemInitialStates(self):
        self.__connected = False
        # self.__disconnect_item.set_active(True)

        access_token = self.__configmanager.access_token
        if access_token is None:
            self.__loggedin = False
            # self.__logout_item.set_active(True)
        else:
            self.__loggedin = True

    def __connectActions(self):
        self.__login_item.connect('activate', self.__login_callback, 'login')
        # self.__logout_item.connect('activate', self.__logout_callback, 'logout')

        # self.__connect_item.connect('activate', self.__connect_callback)
        # self.__disconnect_item.connect('activate', self.__disconnect_callback)

        self.__quit_item.connect('activate', self.__quit_callback)

    def __login_callback(self, item, data=None):
        if self.__login_item.get_active():
            self.__logger.debug('login_item is active')
        else:
            self.__logger.debug('login_item is not active')

        if self.__loggedin:
            return
        else:
            access_token = self.__configmanager.access_token
            if access_token is None:
                self.__oauthgui = OAuthGUI(self.__configmanager, self.__login_done)
                # access_token = self.__configmanager.access_token
                # if access_token is None:
                #     self.__logout_item.set_active(True)
            else:
                self.__loggedin = True

    def __logout_callback(self, item, data=None):
        if self.__logout_item.get_active():
            self.__logger.debug('logout_item is active')
        else:
            self.__logger.debug('logout_item is not active')

        self.__configmanager.logout()

    def __connect_callback(self, item, data=None):
        return

    def __disconnect_callback(self, item, data=None):
        return

    def __quit_callback(self, item, data=None):
        Gtk.main_quit()

    def __login_done(self):
        self.__logger.debug('login done')