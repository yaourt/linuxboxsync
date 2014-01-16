__author__ = 'yaourt'

from gi.repository import Gtk, WebKit, GObject
import urllib
import json
from datetime import datetime, timedelta
import time

class OAuthGUI:
    _loading = """
<html>
<body>
<style>
.bubblingG {
text-align: center;
width:80px;
height:50px;
}

.bubblingG span {
display: inline-block;
vertical-align: middle;
width: 10px;
height: 10px;
margin: 25px auto;
background: #000000;
-moz-border-radius: 50px;
-moz-animation: bubblingG 0.8s infinite alternate;
-webkit-border-radius: 50px;
-webkit-animation: bubblingG 0.8s infinite alternate;
-ms-border-radius: 50px;
-ms-animation: bubblingG 0.8s infinite alternate;
-o-border-radius: 50px;
-o-animation: bubblingG 0.8s infinite alternate;
border-radius: 50px;
animation: bubblingG 0.8s infinite alternate;
}

#bubblingG_1 {
-moz-animation-delay: 0s;
-webkit-animation-delay: 0s;
-ms-animation-delay: 0s;
-o-animation-delay: 0s;
animation-delay: 0s;
}

#bubblingG_2 {
-moz-animation-delay: 0.24s;
-webkit-animation-delay: 0.24s;
-ms-animation-delay: 0.24s;
-o-animation-delay: 0.24s;
animation-delay: 0.24s;
}

#bubblingG_3 {
-moz-animation-delay: 0.48s;
-webkit-animation-delay: 0.48s;
-ms-animation-delay: 0.48s;
-o-animation-delay: 0.48s;
animation-delay: 0.48s;
}

@-moz-keyframes bubblingG {
0% {
width: 10px;
height: 10px;
background-color:#000000;
-moz-transform: translateY(0);
}

100% {
width: 24px;
height: 24px;
background-color:#FFFFFF;
-moz-transform: translateY(-21px);
}

}

@-webkit-keyframes bubblingG {
0% {
width: 10px;
height: 10px;
background-color:#000000;
-webkit-transform: translateY(0);
}

100% {
width: 24px;
height: 24px;
background-color:#FFFFFF;
-webkit-transform: translateY(-21px);
}

}

@-ms-keyframes bubblingG {
0% {
width: 10px;
height: 10px;
background-color:#000000;
-ms-transform: translateY(0);
}

100% {
width: 24px;
height: 24px;
background-color:#FFFFFF;
-ms-transform: translateY(-21px);
}

}

@-o-keyframes bubblingG {
0% {
width: 10px;
height: 10px;
background-color:#000000;
-o-transform: translateY(0);
}

100% {
width: 24px;
height: 24px;
background-color:#FFFFFF;
-o-transform: translateY(-21px);
}

}

@keyframes bubblingG {
0% {
width: 10px;
height: 10px;
background-color:#000000;
transform: translateY(0);
}

100% {
width: 24px;
height: 24px;
background-color:#FFFFFF;
transform: translateY(-21px);
}

}

</style>
<div class="bubblingG" style="width:200px;height:100px;position:absolute;left:50%;top:50%;
margin-left:-100px;margin-top:-50px;">
<span id="bubblingG_1">
</span>
<span id="bubblingG_2">
</span>
<span id="bubblingG_3">
</span>
</div
</body>
</html>
"""
    def __init__(self, config_manager, callback):
        self.__started = False
        self.__config_manager = config_manager
        self.__callback = callback
        w = Gtk.Window()
        w.set_modal(True)
        w.set_title("Box.com login")
        w.set_position(Gtk.WindowPosition.CENTER)
        v = WebKit.WebView()
        self.__v = v
        self.__w = w
        v.can_go_back_or_forward(False)
        sw = Gtk.ScrolledWindow()
        w.add(sw)
        self.__sw = sw
        sw.add(v)
        w.set_size_request(400, 666)
        #w.connect("delete-event", Gtk.main_quit)
        v.connect("resource-request-starting", self.res_change)
        v.connect("context-menu", self.disable_context_menu)
        v.load_string(OAuthGUI._loading, 'text/html', 'UTF-8', '')
        w.show_all()
        GObject.timeout_add(100, self.start)

    def res_change(self, webview, webframe, webresource, req, resp=None, data=None):
        uri = req.get_uri()
        if uri.startswith('oauth:'):
            now = datetime.utcnow()
            state = uri[len('oauth:'):]
            json_data = urllib.unquote(state)

            req.set_uri('about:blank')
            self.__sw.remove(self.__v)

            self.__config_manager._update_from_json(json_data)
            self.__w.destroy()
            self.__callback()

    def disable_context_menu(webview, default_menu, hit_test_result, keyboard_triggered, data):
        return True

    def start(self):
        if self.__started:
            return False
        else:
            self.__v.load_uri('https://linuxboxsyncbridge.appspot.com/')
            self.__started = True

