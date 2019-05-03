import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
import os

# Porfavor hacer esto más seguro
sender_email = "themyscira.io@gmail.com"
password = os.environ.get('CORREO_PW')

"""
    Comprueba que los datos que se le pasan como parámetro sean ambos válidos.
    email - Email que ha introducido el usuario.
    number - El número de pregunta sobre la que activa la notificación
"""
def check_correct_data(email, number):

    # Comprobamos si el email tiene el formato correcto
    if not validate_email(email):
        return False
    
    # Comprobamos si el campo hidden es un numero
    try:
        number = int(number)
    except ValueError:
        return False

    # Devolvemos true en caso de que todos los parámetros sean válidos
    return True

"""
    Envia email a toda la lista de usuarios que se le pasa por parámetro,
    indicandoles que se ha realizado una respuesta a una de las preguntas que activo las notificaiones.
    TODO: Establecer un email html personalizado.
"""
def send_mail_to_notification_list(lista):
    
    # Configuración sobre el mensaje y establecer SSL
    context = ssl.create_default_context()
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"    
    message["From"] = sender_email

    # Cuerpo del mensaje, en texto plano y HTML
    text = """\
    Hey!,
    Tienes un nuevo aviso sobre una pregunta que has marcado."""
    html = """\
    <html>
    <body>
        <h1>Teeeest</h1>
        <a href='https://www.google.es'>Hoooooola</a>
    </body>
    </html>
    """

    # Opciones del mensaje
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    
    # Conecta con la cuenta de GMAIL y se loguea.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)

        # Por cada dirección de correo, envia un mail
        for correo in lista:
            message["To"] = correo
            server.sendmail(sender_email, correo, message.as_string())
