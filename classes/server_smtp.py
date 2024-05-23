import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from os import getenv
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = getenv('SMTP_USER', 'brokerviewes@gmail.com')
SMTP_PASSWORD = getenv('SMTP_PASSWORD', 'wvwx xfvm yzoc aoua')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


class ServerSMTP:

    def send_email(self, to_email, body):

        msg = self.build_message(to_email, body)

        with SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            try:
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, to_email, msg.as_string())
            except smtplib.SMTPException as e:
                print(f"Error al enviar el correo: {e}")

    @staticmethod
    def build_message(to_email, body) -> MIMEMultipart:

        msg = MIMEMultipart()
        msg['From'] = "brokerviewes@gmail.com"
        msg['To'] = to_email
        msg['Subject'] = "Código de verificación"
        msg.attach(MIMEText(body, 'plain'))

        return msg
