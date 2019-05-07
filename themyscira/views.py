from django.contrib.postgres.search import SearchVector
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *

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

# Importa el fichero tools.py que contiene funciones de ayuda.
import sys
sys.path.insert(0, '/tfg/scripts')
from tools import *

def index(request):
    template = loader.get_template('themyscira/index.html')
    context = {
        'test': 'teeeestttt',
    }
    return HttpResponse(template.render(context, request))


"""
    Se ejecuta la siguiente función cuando se entra en el apartado de search/, para ver los videos.
"""
def search(request):

    template = loader.get_template('themyscira/search.html')
    query = request.GET.get('q','')
    data = []

    # En caso de que usemos la barra de búsqueda, entramos en esta parte, sino, muestra todos los videos.
    if query != '':
        end = []
        final = []
        query = query.split()

        # Pasa la query por el algorítmo de filtrado, la cual busca por palabras en el title y tags del video.
        for term in query:
            end.append(Video.objects.annotate(search=SearchVector('title','tags'),).filter(search=term))

        # Agrupa todos los videos que se han encontrado tras el filtrado para ser enviados a la template.
        for queryset in end:
            for video in queryset:
                v = {}
                tmp = {}
                v['video'] = video
                v['autor'] = Autor.objects.get(pk=video.autor_id)
                t = Timestamp.objects.get(pk=video.timestamp_id)
                tmp = dict(zip(t.time,t.data))
                v['timestamp'] = tmp
                data.append(v)

        # Elimina los elementos duplicados en caso de estarlos, por lo que no salen dos videos iguales.
        for element in data:
            if element not in final:
                final.append(element)

        return HttpResponse(template.render({'videos':final,}, request))

    else:

        # Seleccionamos todos los datos de los videos que tenemos asi como sus autores y timestamps correspondientes
        for video in Video.objects.all():
            v = {}
            tmp = {}
            v['video'] = video
            v['autor'] = Autor.objects.get(pk=video.autor_id)
            t = Timestamp.objects.get(pk=video.timestamp_id)
            tmp = dict(zip(t.time,t.data))
            v['timestamp'] = tmp
            data.append(v)

        return HttpResponse(template.render({'videos':data,}, request))

"""
    Se ejecuta cuando vamos a la página de foro/ muestra todas las preguntas y respuestas que tenemos.
"""
def forum(request):
    preguntas = Question.objects.all()
    respuestas = Response.objects.all()
    template = loader.get_template('themyscira/forum.html')
    context = {
        'preguntas': preguntas,
        'respuestas': respuestas,
    }
    return HttpResponse(template.render(context, request))


"""
    Se llama a la siguiente función cuando se envia el formaulario para recibir notificaciones sobre una pregunta.
"""
def getnotify(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Se guardan los datos que envia el form
    user_email = request.POST.get('n-email')
    question = request.POST.get('n-question')

    # Si los datos recibidos no son válidos, se le envia fuera
    if not check_correct_data(user_email, question):
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Comprobamos si la pregunta que se busca existe realmente
    try:
        q = Question.objects.get(pk=question)
    except:
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # En caso de que si exista la pregunta, se le añade el email introducido a la lista en la bd
    q.notificacion_email.append(user_email)
    q.save()

    request.session['has_message'] = good_response

    return HttpResponseRedirect(reverse('themyscira:foro'))

"""
    Se llama a la función cuando se crear una nueva respuesta para una pregunta dada.
    Comprueba que todo sea válido, almacena la respuesta en la bd y envia un correo de notificación a todos los usuarios.
"""
def addresponse(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    user_email = request.POST.get('email-answer-user')
    user_text_response = request.POST.get('text-answer-user')
    question = request.POST.get('q-id')

    # Si los datos recibidos no son válidos, se le envia fuera
    if not check_correct_data(user_email, question):
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Comprobamos si la pregunta que se busca existe realmente
    try:
        q = Question.objects.get(pk=question)
    except:
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Creamos una nueva respuesta y la gurdamos en la bd
    r = Response(question=q, data=user_text_response)
    r.save()

    # En caso de que si exista la pregunta, se le añade el email introducido a la lista en la bd
    q.notificacion_email.append(user_email)
    q.save()

    # Envia un correo de notificación a los usuarios de la lista
    send_mail_to_notification_list(q.notificacion_email)

    request.session['has_message'] = good_response

    return HttpResponseRedirect(reverse('themyscira:foro'))


# TODO: Securizar el input el usuario en el form
def addquestion(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    q_title = request.POST.get('titulo-pregunta')
    q_text = request.POST.get('pregunta-text')

    q = Question(title=q_title, data=q_text, tags=[], notificacion_email=[])
    q.save()

    request.session['has_message'] = good_response
    return HttpResponseRedirect(reverse('themyscira:foro'))

