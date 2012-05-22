#!/usr/bin/env python2
'''
Poll the server for alarms.
'''
from urllib2 import urlopen
import json
import datetime
import os

from app import timeformat
framerate = 60

def loadtime(text):
    return datetime.datetime.strftime(text, timeformat)

while True:
    status = json.loads(urlopen('http://alarm.thomaslevine.com/alarm').read())
    last_alert = loadtime(status['last_alert']) + datetime.timedelta(seconds = framerate)
    current_time = loadtime(status['current_time'])
    if status['status'] != 'okay':
        raise Exception('status')
    elif last_alert > current_time:
        os.system('mplayer ~/Music/Dragonforce/*/*')
    else:
        sleep(framerate)
