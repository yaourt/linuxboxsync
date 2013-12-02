__author__ = 'yaourt'

from gi.repository import Gtk, WebKit
import urllib

class GUI:
    def __init__(self):
        w = Gtk.Window()
        w.set_title("Box.com login")
        w.set_position(Gtk.WindowPosition.CENTER)
        v = WebKit.WebView()
        self.v = v
        self.w = w
        v.can_go_back_or_forward(False)
        sw = Gtk.ScrolledWindow()
        w.add(sw)
        self.sw = sw
        sw.add(v)
        w.set_size_request(400, 666)
        w.connect("delete-event", Gtk.main_quit)
        v.connect("resource-request-starting", self.res_change)
        v.connect("context-menu", self.disable_context_menu)
        v.load_uri('http://127.0.0.1:8080')
        w.show_all()


    def res_change(self, webview, webframe, webresource, req, resp=None, data=None):
        uri = req.get_uri()
        if uri.startswith('oauth:'):
            state = uri[len('oauth:'):]
            print "State: %s" % (urllib.unquote(state))
            req.set_uri('about:blank')
            self.sw.remove(self.v)

    def disable_context_menu(webview, default_menu, hit_test_result, keyboard_triggered, data):
        return True


g = GUI()
Gtk.main()