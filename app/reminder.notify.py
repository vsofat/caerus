import json
import os
import datetime

from utl.notifier import Notifier
from utl.database.models import models
from utl.database.functions.models.users import getAllUsersInfo
from utl.database.functions.models.savedOpportunities import getSavedOpportunities, removeOpportunityReminder
from utl.database.functions.models.savedScholarships import getSavedScholarships, removeScholarshipReminder
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


def findReminderIso(date):
    return (date - datetime.timedelta(days=7)).date().isoformat()


def constructSection(html, l, name):
    if len(l) > 0:
        html += f"<p>Here are all of your favorited {name} that have deadlines next week:</p>"
        for obj in l:
            id = obj.opportunityID if name == 'opportunities' else obj.scholarshipID
            html += f"<a href='{baseurl}/{name}/{id}'>{obj.title}</a><br>"
    return html


def constructBody(opportunities, scholarships, time):
    html = "<html><body>"
    html = constructSection(html, opportunities, 'opportunities')
    html = constructSection(html, scholarships, 'scholarships')
    html += "<br>--<br>Caerus</body></html>"
    return html


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        notifier = Notifier(user, pwd)
        users = getAllUsersInfo()
        for user in users:

            time = datetime.datetime.now()
            iso = time.date().isoformat()

            savedOpps = getSavedOpportunities(user.userID)
            savedScholars = getSavedScholarships(user.userID)

            savedOpps = [opp for opp in savedOpps if opp.deadline != None]
            savedScholars = [s for s in savedScholars if s.deadline != None]

            savedOpps = [
                opp for opp in savedOpps
                if findReminderIso(opp.deadline) == iso
            ]
            savedScholars = [
                s for s in savedScholars
                if findReminderIso(s.deadline) == iso]

            if len(savedOpps) > 0 or len(savedScholars) > 0:
                html = constructBody(savedOpps, savedScholars, time)

                notifier.sendmail(
                    [user.email], f"Caerus Reminder -- {iso}", html
                )
                print(
                    f"Reminder email sent to {user.email} -- {time.isoformat()}")
