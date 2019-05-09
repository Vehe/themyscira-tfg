import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
import os

# Diferentes declaraciones para la notificación al usuario según el resultado.
good_response = {
    'error': 'success-box',
    'face': 'face',
    'status': 'happy',
    'movement': 'scale',
    'error_text': 'Success!',
    'msg': 'yay, todo ha salido bien.',
    'color': 'green'
}

bad_response = {
    'error': 'error-box',
    'face': 'face2',
    'status': 'sad',
    'movement': 'move',
    'error_text': 'Error!',
    'msg': 'oh no, algo ha ido mal.',
    'color': 'red'
}

# Devuelve el texto según el status que se le pasa como parámetro
def get_notification_text(status, msg=''):

    # Comprobamos si se envía un msg o no
    if msg is not'':
        if status:
            good_response['msg'] = msg
            return good_response
        else:
            bad_response['msg'] = msg
            return bad_response

    return good_response if status else bad_response

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
    
    try:
        # Conecta con la cuenta de GMAIL y se loguea.
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)

            # Por cada dirección de correo, envia un mail
            for correo in lista:
                message["To"] = correo
                server.sendmail(sender_email, correo, message.as_string())
    except:
        return False
