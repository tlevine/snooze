#!/usr/bin/env python2
import os
import json
import datetime
import time
import requests

while True:
    text = requests.get('http://search.twitter.com/search.json?q=@thomaslevine+#wakeup&rpp=1&include_entities=true&result_type=mixed').text
    print text
    last_alert = json.loads(text)['created_at']
    half_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes = 0.5)
    if last_alert != None and last_alert > half_minute_ago:
        os.system('mplayer ~/Music/DragonForce/*/*')
    else:
        time.sleep(30)
