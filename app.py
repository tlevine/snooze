#!/usr/bin/env python2

import datetime
import web
from dumptruck import DumpTruck
import json

urls = (
    '/', 'index',
    '/alarm', 'alarm'
)

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

class alarm:
    def GET(self):
        web.header('Content-Type', 'application/json')
        try:
            dt = connect_db()
            last_alert = dt.execute('select datetime from alarms order by datetime desc limit 1')[0]['datetime']
        except IndexError:
            return '{"status": "okay", "last_alert": null}'
        else:
            return json.dumps({
                'status': 'okay',
                'last_alert': last_alert.isoformat(),
                'current_time': datetime.datetime.now().isoformat(),
            })

    def POST(self):
        web.header('Content-Type', 'application/json')
        now = datetime.datetime.now()
        dt = connect_db()
        dt.insert({'datetime': now}, 'alarms')
        return json.dumps({'status': 'okay', 'current_alert': now})

def connect_db():
    return DumpTruck(dbname = 'snooze.sqlite')

def create_db():
    dt = connect_db()
    dt.create_table({'datetime': datetime.datetime.now()}, 'alarms', if_not_exists = True)
    dt.create_index('alarms', ['datetime'], unique = True)

create_db()
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
