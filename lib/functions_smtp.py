from classes.server_smtp import ServerSMTP


def send_email(to_email: str, code: str):

    body = f"Tú código de verificación es: {code}"

    server = ServerSMTP()
    server.send_email(to_email=to_email, body=body)
