import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user = ''
pwd = ''


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
            msg['From'] = ''
            msg['To'] = recipient

            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            self.server.sendmail(self.username, recipient, msg.as_string())


notifier = Notifier(user, pwd)
notifier.sendmail([''], 'Special Delivery', "My name is my name.")

# https://support.google.com/mail/answer/7126229?p=BadCredentials&visit_id=637267656946578056-6078978&rd=2#cantsignin
# https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804
# https://realpython.com/python-send-email/
