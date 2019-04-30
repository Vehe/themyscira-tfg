from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *

import sys
sys.path.insert(0, '/tfg/tools')
from tools import *

def index(request):
    template = loader.get_template('themyscira/index.html')
    context = {
        'test': 'teeeestttt',
    }
    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template('themyscira/search.html')
    context = {
        'test': 'teeeestttt',
    }
    return HttpResponse(template.render(context, request))

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
    TODO: Configurar los argumentos que se devuelven al hacer el reverse, fixear el codigo 400.
"""
def getnotify(request):
    
    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        return HttpResponse(status=400)

    # Se guardan los datos que envia el form
    user_email = request.POST.get('n-email')
    question = request.POST.get('n-question')
    
    # Si los datos recibidos no son válidos, se le envia fuera
    if not check_correct_data(user_email, question):
        return HttpResponse(status=400)

    # Comprobamos si la pregunta que se busca existe realmente
    try:
        q = Question.objects.get(pk=question)
    except:
        return HttpResponse(status=400)

    # En caso de que si exista la pregunta, se le añade el email introducido a la lista en la bd
    q.notificacion_email.append(user_email)
    q.save()
    
    return HttpResponseRedirect(reverse('themyscira:foro'))

"""
    Se llama a la función cuando se crear una nueva respuesta para una pregunta dada.
    Comprueba que todo sea válido, almacena la respuesta en la bd y envia un correo de notificación a todos los usuarios.
"""
def addresponse(request):

    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        return HttpResponse(status=400)

    user_email = request.POST.get('email-answer-user')
    user_text_response = request.POST.get('text-answer-user')
    question = request.POST.get('q-id')

    # Si los datos recibidos no son válidos, se le envia fuera
    if not check_correct_data(user_email, question):
        return HttpResponse(status=400)

    # Comprobamos si la pregunta que se busca existe realmente
    try:
        q = Question.objects.get(pk=question)
    except:
        return HttpResponse(status=400)

    # Creamos una nueva respuesta y la gurdamos en la bd
    r = Response(question=q, data=user_text_response)
    r.save()

    # En caso de que si exista la pregunta, se le añade el email introducido a la lista en la bd
    q.notificacion_email.append(user_email)
    q.save()

    # Envia un correo de notificación a los usuarios de la lista
    send_mail_to_notification_list(q.notificacion_email)

    return HttpResponseRedirect(reverse('themyscira:foro'))
