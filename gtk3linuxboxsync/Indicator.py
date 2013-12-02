__author__ = 'yaourt'

import os
from gi.repository import Gtk

try:
    from gi.repository import AppIndicator3  # @UnresolvedImport
    HAS_INDICATOR=True
except:
    HAS_INDICATOR=False

class Indicator(object):
    def __init__(self, menu):
        _cur_dir = os.path.dirname(__file__)
        self.ind = AppIndicator3.Indicator.new (
                          "thetool",
                          "",
                          AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)
        iconpath = os.path.join(_cur_dir, 'b64.png')
        self.ind.set_icon(iconpath)
        iconpath_active=os.path.join(_cur_dir, 'b64-active.png')
        self.ind.set_attention_icon (iconpath_active)
        self.ind.set_menu(menu)

    def set_label(self, txt):
        self.ind.set_label(txt, txt)

    def set_attention(self, attention):
        if attention:
            self.ind.set_status (AppIndicator3.IndicatorStatus.ATTENTION)
        else:
            self.ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)


menu = Gtk.Menu()
item = Gtk.MenuItem()
item.set_label("Menu Item")
item.show()
menu.append(item)

menu.show()
i= Indicator(menu)
i.set_attention(True)

Gtk.main()
