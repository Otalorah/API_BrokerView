from classes.server_smtp import ServerSMTP


def send_email(email: str, code: str):

    body = f"""Hola,
    
Recientemente recibió instrucciones para ingresar un código de autenticación en su cuenta BrokerView.

Su código de verificación es: {code}"""

    server = ServerSMTP()
    server.send_email(email=email, body=body)
