import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import datetime

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


class Notifier:
    def __init__(self, username, password, host='smtp.gmail.com', port=587):
        self.username = username
        self.password = password
        self.host = host

        self.server = smtplib.SMTP(host, port)
        self.server.starttls()
        self.server.login(username, password)

    def constructBody(self, opportunities, preferences):
        hasNoPreferences = [len(preferences[key]) == 0 for key in preferences.keys()]
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

    def sendmail(self, recipients, subject, html):
        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = 'caerus.stuy@gmail.com'
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(html, "html"))

            self.server.sendmail(self.username, recipient, msg.as_string())


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
            html = notifier.constructBody(opps, prefs)

            time = datetime.datetime.now()
            notifier.sendmail(
                [email], f"Caerus Weekly Update -- {time.date().isoformat()}", html
            )
            print(f"Sent email to {email} -- {time.isoformat()}")
