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
    status = json.loads(urlopen('http://alarm.thomaslevine.com/page').read())
    last_alert = loadtime(status['last_alert']) + datetime.timedelta(seconds = framerate)
    current_time = loadtime(status['current_time'])

    music = status['music']

    if status['status'] != 'okay':
        raise Exception('status')
    elif music not in music_choices:
        raise ValueError('The music choice "%s" is not among the options.' % music)
    elif last_alert > current_time:
        os.system('mplayer ~/Music/%s/*/* &>/dev/null &' % music)
        raw_input('You are being summoned! Press any key to stop the music')
        os.system('killall mplayer')
    else:
        print('No alarm')

    sleep(framerate)
