__author__ = 'yaourt'

from unittest import TestCase
import time
import os

import pyinotify
import tempfile

from gtk3linuxboxsync.BoxLocalDirectoryWatcher import BoxLocalDirectoryWatcher

class TestBoxLocalDirectoryWatcher(TestCase):
    def test_startAndStop(self):
        class EventHandler(pyinotify.ProcessEvent):
            def __init__(self):
                self.created = 0
                self.deleted = 0

            def process_IN_CREATE(self, event):
                print "Creating:", event.pathname
                self.created += 1

            def process_IN_DELETE(self, event):
                print "Removing:", event.pathname
                self.deleted +=1

        event_processor = EventHandler()
        w = BoxLocalDirectoryWatcher(event_processor)
        w.start()
        utest_folder = tempfile.mkdtemp(dir=w.box_dir)
        utest_subfolder = os.path.join(utest_folder, 'subfolder')
        os.makedirs(utest_subfolder)
        time.sleep(1)
        os.rmdir(utest_subfolder)
        os.rmdir(utest_folder)
        time.sleep(1)
        assert event_processor.created == 2
        assert event_processor.deleted == 2

        w.stop()