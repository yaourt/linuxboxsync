__author__ = 'yaourt'

import os
from gi.repository import Gtk

try:
    from gi.repository import AppIndicator3  # @UnresolvedImport
    HAS_INDICATOR=True
except:
    HAS_INDICATOR=False

class Indicator(object):


    def __init__(self):
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
        menu = Gtk.Menu()
        attention_item = Gtk.CheckMenuItem('Attention')
        attention_item.show()
        attention_item.connect('activate', self.swap_attention)
        menu.append(attention_item)

        quit_item = Gtk.CheckMenuItem('Quit')
        quit_item.show()
        quit_item.connect('activate', self.quit)
        menu.append(quit_item)
        self.ind.set_menu(menu)

    def set_label(self, txt):
        self.ind.set_label(txt, txt)

    def set_attention(self, attention):
        if attention:
            self.ind.set_status (AppIndicator3.IndicatorStatus.ATTENTION)
            #self.ind.set_label("Attention Label 01234567890123456789012345678901234567890123456789012345678901234567890123456789", "")
        else:
            self.ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)
            #self.ind.set_label("", "")

    def swap_attention(self, item):
        self.set_attention(item.get_active())

    def quit(self, item):
        Gtk.main_quit()

i = Indicator()
Gtk.main()
