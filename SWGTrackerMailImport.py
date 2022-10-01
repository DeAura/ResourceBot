from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import utils.auth as auth
import time
import logging, sys
import configparser
import json
import os
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class OnMyWatch:
	# Set the directory on watch
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
    watchDirectory = config.get('swg-scanner', 'mailPath')
    print(watchDirectory)
    print('ready for scanning..')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
            exit()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # new mail, get it and get our userID..
            config = configparser.ConfigParser()
            config.read_file(open(r'config.txt'))
            scannerUserID = config.get('swg-scanner', 'scannerUserID')
            scannerUserKey = config.get('swg-scanner', 'scannerUserKey')

            print("Watchdog received created event - % s." % event.src_path)
            with open(event.src_path) as f:
                contents = f.read()
                print(contents)
                data = {
                    'incomingData': contents,
                    'scannerUserID': scannerUserID,
                    'scannerUserKey': scannerUserKey
                }
                json_content = json.dumps(data)
                resp = auth.send_mailContent(json_content)
                print(resp)


def main_process():
    return 1

while True:
    watch = OnMyWatch()
    watch.run()