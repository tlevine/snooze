#!/usr/bin/env python2
import os
import json
import datetime
import urllib2
import time

while True:
    last_alert = json.loads(urllib2.urlopen('http://alarm.thomaslevine.com/alarm').read())['last_alert']
    half_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes = 0.5)
    if last_alert != None and last_alert > half_minute_ago:
        os.system('mplayer ~/Music/DragonForce/*/*')
    else:
        time.sleep(30)
