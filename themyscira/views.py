from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *
import requests as rq
import random
import json

# Importa el fichero tools.py que contiene funciones de ayuda.
import sys
sys.path.insert(0, '/tfg/scripts')
from tools import *

"""
    Se ejecuta cuando se pide la página principal de la web.
    Muestra el template index.html.
"""
def index(request):

    template = loader.get_template('themyscira/index.html')

    # Variables
    context = {}
    live = []

    # Guardamos la cabecera para la peticion.
    auth_header = {'Client-ID': 'shvvm6arui2mnb87xh6tqrb5i0zz4z'}

    # Descargamos un JSON todos los streams de Science and Technology.
    r = rq.get('https://api.twitch.tv/helix/streams?game_id=509670', headers=auth_header)
    data = json.loads(json.dumps(r.json()))

    # Por cada canal en directo, buscamos alguno que esté haciendo programacion.
    for channel in data['data']:
        if 'a59f1e4e-257b-4bd0-90c7-189c3efbf917' in channel['tag_ids']:
            live.append( { 'user_id': channel['user_id'], 'title': channel['title'] } )

    # Selecionamos un streaming aleatoriamente.
    context.update(random.choice(live))

    # Almacenamos informacion sobre el usuario del stream seleccionado.
    r = rq.get('https://api.twitch.tv/helix/users?id=' + context['user_id'], headers=auth_header)
    data = json.loads(json.dumps(r.json()))

    # Agurpamos toda la informacion sobre el usuario para enviarla al template.
    context.update(data['data'][0])

    return HttpResponse(template.render({'streamer': context,}, request))


"""
    Se ejecuta cuando se entra a la sección de contacto en la web.
    Devuelve el template contacto.html con la variable autores que contiene todos los autores de la bd.
"""
def contacto(request):
    template = loader.get_template('themyscira/contacto.html')
    data = Autor.objects.all()
    return HttpResponse(template.render({'autores':data,}, request))


"""
    Se ejecuta cuando se envía el form de la pestaña de contacto (autor), se guardan todos los parámetros,
    se comprueba que ese autor no existe en la base de datos, y se crea un nuevo RequestAutor para que 
    los miembros del staff den el visto bueno.
"""
def addautor(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le devuelve a la pestaña de contacto.
    if request.method != 'POST':
        request.session['has_message'] = get_notification_text(False, 'Buen intento  (ノಠ益ಠ)ノ彡┻━┻')
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # Almacenamos los datos que entran por el form.
    autor_name = request.POST.get('name','')
    youtube = request.POST.get('youtube','')
    twitch = request.POST.get('twitch','')
    twitter = request.POST.get('twitter','')
    github = request.POST.get('github','')

    # En caso de que el nombre esté vacío, se le envía a la página de contacto.
    if autor_name == '':
        request.session['has_message'] = get_notification_text(False, 'oh no, parece que olvidaste el nombre.')
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # En caso de que ya exista un usuario con ese nombre, volvemos al contacto.
    try:
        a = Autor.objects.get(name=autor_name)
    except:

        # En caso de que todo haya ido bien, guardamos el autor en la tabla de requests y redirigimos al user a la página contacto.
        r = RequestAutor(name=autor_name, twitter=twitter, twitch=twitch, youtube=youtube, github=github)
        r.save()

        request.session['has_message'] = get_notification_text(True)
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # Si ha llegado aqui, significa que el usuario que ha introducido ya existía, por lo que no se hace nada.
    request.session['has_message'] = get_notification_text(False, 'oh no, este autor ya existe!')
    return HttpResponseRedirect(reverse('themyscira:contacto'))


"""
    Se ejecuta cuando se envía el form de la pestaña de contacto (video), se guardan todos los parámetros,
    se comprueba que ese video no existe en la base de datos, y se crea un nuevo RequestVideo para que 
    los miembros del staff den el visto bueno.
"""
def addvideo(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le devuelve a la pestaña de contacto.
    if request.method != 'POST':
        request.session['has_message'] = get_notification_text(False, 'Buen intento  (ノಠ益ಠ)ノ彡┻━┻')
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # Almacenamos los parámetros que nos envia el form
    v_url = request.POST.get('url','')
    v_title = request.POST.get('title','')
    v_autor = request.POST.get('autor','')
    v_tags = request.POST.get('tags','')
    v_time = request.POST.get('time','')
    v_data = request.POST.get('data','')

    # Comprobamos si existe algún autor con el nombre que se nos ha pasado
    try:
        a = Autor.objects.get(name=v_autor)
    except:
        request.session['has_message'] = get_notification_text(False, 'oh no, el autor no existe.')
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # Convertimos los siguientes parámetros en arrays
    v_tags = v_tags.split(',')
    v_time = v_time.split(',')
    v_data = v_data.split(',')
    v_url = v_url.split('v=')

    # Comprobamos si la url es válida (URL completa), en caso de no serlo, volvemos a la pestaña de contacto.
    if len(v_url) < 2:
        request.session['has_message'] = get_notification_text(False, 'oh no, la url no es válida.')
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # Comprobamos si el video ya existe en la base de datos.
    try:
        v = Video.objects.get(url=v_url[1])
    except:
        # Se ejecuta en caso de que el vídeo no esté en la base de datos, así que creamos un request para posterior revisión.
        video = RequestVideo(url=v_url[1], title=v_title, autor=a, tags=v_tags, timestamp_time=v_time, timestamp_data=v_data)
        video.save()

        request.session['has_message'] = get_notification_text(True)
        return HttpResponseRedirect(reverse('themyscira:contacto'))

    # En caso de que este aqui, quiere decir que ya existe ese video, por lo que no se hace nada.
    request.session['has_message'] = get_notification_text(False, 'oh no, el video introducido ya existe.')
    return HttpResponseRedirect(reverse('themyscira:contacto'))


"""
    Para acceder a esta ventana tenemos que tener permisos de staff, nos muestra en formato
    web las requests de videos y autores que nos han hecho los usuarios.
"""
@user_passes_test(lambda u: u.is_staff)
def requests(request):
    template = loader.get_template('themyscira/requests.html')
    a = RequestAutor.objects.all()
    v = RequestVideo.objects.all()
    return HttpResponse(template.render({'autores':a,'videos':v,}, request))


"""
    Se ejecuta cuando se envía el form de la pestaña requests seccion autor, su función es borrar el request o 
    aceptarlo y pasar de ser un RequestAutor a Autor.
"""
@user_passes_test(lambda u: u.is_staff)
def raddautor(request):

    # En caso de que no sea post, se le devuelve a la pestaña requests.
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Almacenamos los datos que entran por el form.
    ra_id = request.POST.get('id','')
    tipo = request.POST.get('tipo','')

    # En caso de que alguno de los parámetros sea no válido, volvemos a la página requests.
    if ra_id == '' or tipo == "":
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Comprobamos si realmente existe este request de autor, en caso de no existir, volvemos a la pestaña requests.
    try:
        a = RequestAutor.objects.get(pk=ra_id)
    except:
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Comprobamos el tipo de petición que se quiere, si aceptar, descartar o petición desconocida.
    if tipo == 'accept':
        # Convierte el RequestAutor en Autor, y elimina el request.
        new = Autor(name=a.name, youtube=a.youtube, twitter=a.twitter, twitch=a.twitch, github=a.github)
        new.save()
        a.delete()
        return HttpResponseRedirect(reverse('themyscira:requests'))
    elif tipo == 'delete':
        # Elimina la entrada en RequestAutor.
        a.delete()
        return HttpResponseRedirect(reverse('themyscira:requests'))
    else:
        # Se ha realizado una petición desconocida, por lo que se vuelve a la pestaña requests sin hacer cambios.
        return HttpResponseRedirect(reverse('themyscira:requests'))


"""
    Se ejecuta cuando se envía el form de la pestaña requests seccion video, su función es borrar el request o 
    aceptarlo y pasar de ser un RequestVideo a Video.
"""
@user_passes_test(lambda u: u.is_staff)
def raddvideo(request):

    # En caso de que no sea post, se le devuelve a la pestaña requests.
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Almacenamos los datos que entran por el form.
    ra_id = request.POST.get('id','')
    tipo = request.POST.get('tipo','')

    # En caso de que alguno de los parámetros sea no válido, volvemos a la página requests.
    if ra_id == '' or tipo == "":
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Comprobamos si realmente existe este RequestVideo.
    try:
        a = RequestVideo.objects.get(pk=ra_id)
    except:
        return HttpResponseRedirect(reverse('themyscira:requests'))

    # Comprobamos el tipo de petición que se quiere, si aceptar, descartar o petición desconocida.
    if tipo == 'accept':
        # Crea un Timesamp y crea el Video asociandole este Timestamp.
        t = Timestamp(time=a.timestamp_time, data=a.timestamp_data)
        t.save()
        v = Video(url=a.url, tags=a.tags, title=a.title, autor=a.autor, timestamp=t)
        v.save()
        a.delete()
        return HttpResponseRedirect(reverse('themyscira:requests'))
    elif tipo == 'delete':
        # Elimina la entrada en RequestAutor.
        a.delete()
        return HttpResponseRedirect(reverse('themyscira:requests'))
    else:
        # Se ha realizado una petición desconocida, por lo que se vuelve a la pestaña requests sin hacer cambios.
        return HttpResponseRedirect(reverse('themyscira:requests'))


"""
    Se ejecuta la siguiente función cuando se entra en el apartado de search/, para ver los videos.
    Si se envía una petición GET con el parámetro q y este no está vacío, se usa un algorítmo de búsqueda sobre el 
    titulo y los tag del video por probabilidad, en caso de estar vacío o no estar, se muestran todos los videos.
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
    template = loader.get_template('themyscira/forum.html')
    preguntas = Question.objects.all()
    respuestas = Response.objects.all()
    return HttpResponse(template.render({'preguntas':preguntas, 'respuestas':respuestas,}, request))


"""
    Se llama a la siguiente función cuando se envia el formaulario para recibir notificaciones sobre una pregunta.
"""
def getnotify(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le envía de nuevo al foro.
    if request.method != 'POST':
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Se guardan los datos que envía el form.
    user_email = request.POST.get('n-email')
    question = request.POST.get('n-question')

    # Si los datos recibidos no son válidos, se le envia de nuevo al foro.
    if not check_correct_data(user_email, question):
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Comprobamos si la pregunta que se busca existe realmente.
    try:
        q = Question.objects.get(pk=question)
    except:
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # En caso de que si exista la pregunta, se le añade el email introducido a la lista en la bd.
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

    # Envia un correo de notificación a los usuarios de la lista
    send_mail_to_notification_list(q.notificacion_email)

    # En caso de que si exista la pregunta, se le a  ade el email introducido a la lista en la bd
    q.notificacion_email.append(user_email)
    q.save()

    request.session['has_message'] = good_response

    return HttpResponseRedirect(reverse('themyscira:foro'))


"""
    Se ejecuta cuando se desea añadir una nueva pregunta al foro.
"""
def addquestion(request):

    request.session.set_expiry(2)

    # En caso de que no sea post, se le envia fuera
    if request.method != 'POST':
        request.session['has_message'] = bad_response
        return HttpResponseRedirect(reverse('themyscira:foro'))

    # Guarda los parámetros enviados por el form
    q_title = request.POST.get('titulo-pregunta')
    q_text = request.POST.get('pregunta-text')

    # Crea una nueva Question y la guarda en la bd.
    q = Question(title=q_title, data=q_text, tags=[], notificacion_email=[])
    q.save()

    request.session['has_message'] = good_response
    return HttpResponseRedirect(reverse('themyscira:foro'))

