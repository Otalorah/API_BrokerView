from smtplib import SMTP_SSL

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os import getenv
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = getenv('SMTP_USER')
SMTP_PASSWORD = getenv('SMTP_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


class ServerSMTP:

    def send_email(self, email, body):

        msg = self.build_message(email, body)

        with SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, msg.as_string())

    @staticmethod
    def build_message(email, body) -> MIMEMultipart:

        msg = MIMEMultipart()
        msg['From'] = "brokerviewes@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Código de verificación"
        msg.attach(MIMEText(body, 'plain'))

        return msg
