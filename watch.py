#!/usr/bin/env python2
'''
Poll the server for alarms.
'''
from urllib2 import urlopen
import json
import datetime
import os
from time import sleep

from app import timeformat, music_choices
framerate = 10

def loadtime(text):
    return datetime.datetime.strptime(text, timeformat)

while True:
    print chr(27) + "[2J" #Clear terminal
    print datetime.datetime.now().strftime(timeformat)
    status = json.loads(urlopen('http://alarm.thomaslevine.com/alarm').read())
    last_alert = loadtime(status['last_alert']) + datetime.timedelta(seconds = framerate)
    current_time = loadtime(status['current_time'])
    if status['status'] != 'okay':
        raise Exception('status')
    elif last_alert > current_time:
        print('<blinking lights>')
        os.system('mplayer ~/Music/DragonForce/*/* &>/dev/null &')
        raw_input('You are being summoned! Press any key to stop the music')
        os.system('killall mplayer')
    else:
        print('No alarm')
        sleep(framerate)
