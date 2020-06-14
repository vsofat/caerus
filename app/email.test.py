import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os

from utl.database.functions.models.preferences import getPreferredOpportunitiesForAllUsers
from utl.database.models import models
from __init__ import app

db = models.db

path = os.path.dirname(__file__) + "/../gmail.json"
f = json.load(path)

user = f['gmail']
pwd = f['password']


class Notifier:
    def __init__(self, username, password, host='smtp.gmail.com', port=587):
        self.username = username
        self.password = password
        self.host = host

        self.server = smtplib.SMTP(host, port)
        self.server.starttls()
        self.server.login(username, password)

    def sendmail(self, recipients, subject, body):
        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = 'caerus.stuy@gmail.com'
            msg['To'] = recipient

            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            self.server.sendmail(self.username, recipient, msg.as_string())


# notifier.sendmail(['elau00@stuy.edu'], 'Special Delivery', "My name is my name.")
# https://support.google.com/mail/answer/7126229?p=BadCredentials&visit_id=637267656946578056-6078978&rd=2#cantsignin
# https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804
# https://realpython.com/python-send-email/

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        info = getPreferredOpportunitiesForAllUsers()
        notifier = Notifier(user, pwd)
        print(info)
