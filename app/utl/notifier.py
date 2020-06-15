import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
            msg['From'] = self.username
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(html, "html"))

            self.server.sendmail(self.username, recipient, msg.as_string())
