__author__ = 'yaourt'

import subprocess
import os

import pyinotify


class BoxLocalDirectoryWatcher:
    """Manage the event related to the local Box directory"""

    def __init__(self, eventProcessor):
        self.eventProcessor = eventProcessor
        desktop_dir = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).strip()
        self.box_dir = os.path.join(desktop_dir, 'Box')
        if not os.path.exists(self.box_dir):
            os.makedirs(self.box_dir)

        self.watch_manager = pyinotify.WatchManager()
        self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
        BoxLocalDirectoryWatcher._instance = self

    def start(self):
        """Start the watcher"""
        notifier = pyinotify.ThreadedNotifier(self.watch_manager, self.eventProcessor)
        wdd = self.watch_manager.add_watch(self.box_dir, self.mask, rec=True, auto_add=True)
        self.watch_descriptor = wdd
        self.notifier = notifier
        notifier.start()

    def stop(self):
        """Stop the watcher"""
        self.watch_manager.rm_watch(self.watch_descriptor[self.box_dir], rec=True)
        self.notifier.stop()
