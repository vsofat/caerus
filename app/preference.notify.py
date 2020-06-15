import json
import os
import datetime

from utl.notifier import Notifier
from utl.database.functions.models.preferences import getPreferredOpportunitiesForAllUsers, getAllPreferences
from utl.database.models import models
from __init__ import app

db = models.db

DIR = os.path.dirname(__file__) or "."
DIR += "/"
path = DIR + "../gmail.json"

f = open(path)
f = json.load(f)

user = f['gmail']
pwd = f['password']

baseurl = "http://127.0.0.1:5000"


def constructBody(opportunities, preferences):
    hasNoPreferences = [len(preferences[key]) ==
                        0 for key in preferences.keys()]
    hasNoPreferences = True if not False in hasNoPreferences else False

    intro = 'Here are all the new opportunities posted on Caerus within the past week that you might be interested in:'
    if hasNoPreferences:
        intro = f"""
                You have not set any preferences for types of opportunities you'd like to receive emails for.
                Consider setting your preferences <a href='{baseurl}/preferences'>here</a>. <br>
                Here are all of the new opportunities posted on Caerus within the past week:"""

    html = f"<html><body><p>{intro}<p>"

    for opportunity in opportunities:
        html += f"<a href='{baseurl}/opportunities/{opportunity.opportunityID}'>{opportunity.title}</a><br>"

    html += "<br>--<br>Caerus</body></html>"

    return html


# https://support.google.com/mail/answer/7126229?p=BadCredentials&visit_id=637267656946578056-6078978&rd=2#cantsignin
# https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804
# https://realpython.com/python-send-email/

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        info = getPreferredOpportunitiesForAllUsers()
        notifier = Notifier(user, pwd)
        for email in info.keys():
            prefs = getAllPreferences(info[email]['id'])
            opps = info[email]['opportunities']
            if len(opps) > 0:
                html = constructBody(opps, prefs)

                time = datetime.datetime.now()
                notifier.sendmail(
                    [email], f"Caerus Weekly Update -- {time.date().isoformat()}", html
                )
                print(f"Notification email sent to {email} -- {time.isoformat()}")
