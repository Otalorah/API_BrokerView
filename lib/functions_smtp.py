from classes.server_smtp import ServerSMTP


def send_email(email: str, code: str):

    body = f"Tú código de verificación es: {code}"

    server = ServerSMTP()
    server.send_email(to_email=email, body=body)
