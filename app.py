#!/usr/bin/env python2

import datetime
import web
from dumptruck import DumpTruck
import json

urls = (
    '/', 'index',
    '/alarm', 'alarm'
)
timeformat = '%A, %B %d, %Y at %H:%M:%S'
music_choices = ['DragonForce', 'Skream']

class index:
    def GET(self):
        return '''
<style>form, input { display: inline; }</style>
<h1>Wake Tom up.</h1>
<p>
  I've wanted to make this for years. My bed is next to my computer,
  and I leave my speakers on, so you can wake me up any time.
</p>
<h2>Directions</h2>
<ul>
  <li>
    <form action="/alarm" method="get"><input type="submit" value="GET"></form>
    to /alarm to see when the last alarm was started.
  </li>
  <li>
    <form action="/alarm" method="post"><input type="submit" value="POST"></form>
     to /alarm to play loud music from Tom's speakers.
  </li>
</ul>
'''

class db:
    def GET(self):
        raise web.seeother('snooze.sqlite')

class alarm:
    def GET(self):
        web.header('Content-Type', 'application/json')
        alarm_request = dt.execute('select music, datetime from alarms order by datetime desc limit 1')[0]
        try:
            alarm_request['datetime']
        except IndexError:
            return '{"status": "okay", "last_alert": null}'
        else:
            return json.dumps({
                'status': 'okay',
                'last_alert': alarm_request['datetime'].strftime(timeformat),
                'current_time': datetime.datetime.now().strftime(timeformat),
                'music': alarm_request['music'],
            })

    def POST(self):
        web.header('Content-Type', 'application/json')
        music = web.input().get('music', 'DragonForce')

        if music not in music_choices:
            return json.dumps({
               'status': "Music must be one of the choices listed in the 'music_choices' field",
               'music_choices': music_choices,
            })

        now = datetime.datetime.now()
        dt.insert({'datetime': now, 'music': music}, 'alarms')
        return json.dumps({
            'status': 'okay',
            'current_alert': now.strftime(timeformat),
            'music': music
        })


def create_db():
    dt = connect_db()
    dt.create_table({
        'datetime': datetime.datetime.now(),
        'music': 'DragonForce'
    }, 'alarms', if_not_exists = True)
    dt.create_index('alarms', ['datetime'], unique = True)



# Server and a hack for database location and timeformat passing
try:
    dt = DumpTruck(dbname = '/srv/www/snooze/snooze.sqlite')
except:
    app = web.application(urls, globals())
    dt = DumpTruck(dbname = 'snooze.sqlite')
    app = web.application(urls, globals())
else:
    app = web.application(urls, globals())
    application = app.wsgifunc()
