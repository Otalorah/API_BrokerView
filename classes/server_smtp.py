from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')
FROM_EMAIL = getenv('FROM_EMAIL', 'brokerviewes@gmail.com')


class ServerSMTP:
    def send_email(self, email: str, body: str):
        """
        Envía un email usando SendGrid API
        """
        try:
            message = Mail(
                from_email=Email(FROM_EMAIL),
                to_emails=To(email),
                subject='Código de verificación',
                plain_text_content=Content("text/plain", body)
            )
            
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            
            print(f"✅ Email enviado exitosamente! Status: {response.status_code}")
            return response
            
        except Exception as e:
            print(f"❌ Error enviando email: {str(e)}")
            raise e
    
    @staticmethod
    def build_message(email, body):
        """
        Método mantenido por compatibilidad pero ya no es necesario
        SendGrid maneja la construcción del mensaje internamente
        """
        pass