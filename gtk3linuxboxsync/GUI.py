__author__ = 'yaourt'

from gi.repository import Gtk, WebKit

class GUI:
    def __init__(self):
        w = Gtk.Window()
        v = WebKit.WebView()
        v.can_go_back_or_forward(False)
        sw = Gtk.ScrolledWindow()
        w.add(sw)
        sw.add(v)
        w.set_size_request(400, 700)
        w.connect("destroy", lambda q: Gtk.main_quit())
        v.connect("resource-request-starting", self.res_change)
        v.connect("context-menu", self.disable_context_menu)
        v.load_uri('http://127.0.0.1:8080')
        w.show_all()
        Gtk.main()

    def res_change(self, webview, webframe, webresource, req, resp=None, data=None):
        uri = req.get_uri()
        if uri.startswith('oauth://'):
            state = uri[len('oauth://'):]
            print "State: %s" % (state)
            req.set_uri("about:blank")

    def disable_context_menu(webview, default_menu, hit_test_result, keyboard_triggered, data):
        return True

g = GUI()