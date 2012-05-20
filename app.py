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
        web.header('Content-Type', 'application/json')
        return json.dumps({
            'description': 'Wake Tom up.',
            'about': 'I\'ve wanted to make this for years. My bed is next to my computer, and I leave my speakers on, so you can wake me up any time.',
            'directions': 'POST to /alarm to play loud music from Tom\'s speakers. GET to /alarm to see when the last alarm was started.',
        })

class alarm:
    def GET(self):
        web.header('Content-Type', 'application/json')
        try:
            last_alert = dt.execute('select datetime from alarms order by date desc limit 1')[0]['datetime']
        except IndexError:
            return '{"status": "okay", "last_alert": null}'
        else:
            return json.dumps({'status': 'okay', 'last_alert': last_alert})

    def POST(self):
        web.header('Content-Type', 'application/json')
        now = datetime.datetime.now()
        dt.insert({'datetime': now}, 'alarms')
        return json.dumps({'status': 'okay', 'current_alert': now})

if __name__ == "__main__":
    dt = DumpTruck(dbname = 'snooze.sqlite')
    dt.create_table({'datetime': datetime.datetime.now()}, 'alarms', if_not_exists = True)
    dt.create_index('alarms', ['datetime'], unique = True)

    app = web.application(urls, globals())
    app.run()