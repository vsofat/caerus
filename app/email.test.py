import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import datetime

from utl.database.functions.models.preferences import getPreferredOpportunitiesForAllUsers
from utl.database.models import models
from __init__ import app

db = models.db

path = os.path.dirname(__file__) + "/../gmail.json"
f = open(path)
f = json.load(f)

user = f['gmail']
pwd = f['password']

intro = "Here are all the new opportunities posted on Caerus within the past week that you might be interested in:"
baseurl = "http://127.0.0.1:5000"

class Notifier:
    def __init__(self, username, password, host='smtp.gmail.com', port=587):
        self.username = username
        self.password = password
        self.host = host

        self.server = smtplib.SMTP(host, port)
        self.server.starttls()
        self.server.login(username, password)

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
        for user in info.keys():
            opps = info[user]
            if len(opps) > 0:
                html = f"""
                <html>
                    <body>
                        <p>{intro}</p><br>
                """
                for opp in opps:
                    html += f"""
                        <b><a href="{baseurl}/opportunities/{opp.opportunityID}">{opp.title}</a></b>
                    """
                html += """
                    </body>
                </html>
                """
                time = datetime.datetime.now()
                notifier.sendmail([user], f"Caerus Weekly Update -- {time.date().isoformat()}", html)
                print(f"Sent email to {user} -- {time.isoformat()}")