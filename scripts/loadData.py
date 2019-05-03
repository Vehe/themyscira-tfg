import json
from themyscira.models import *

# Abre el fichero JSON que contiene toda la base de datos para estos ser insertados en sus respecitvas tablas.
with open('/tfg/scripts/database.json') as json_file:
    data = json.load(json_file)

    # Carga en la base de datos todo lo correspondiente a la parte del foro de la web, preguntas y respuestas.
    for question in data['questions']:
        q = Question(title=question['title'], data=question['data'], tags=question['tags'], notificacion_email=question['notificacion_email'])
        q.save()
        for response in question['responses']:
            r = Response(data=response, question_id=q.id)
            r.save()

    # Carga en la base de datos todo lo correspondiente a la parte de videos de la web, autores, videos y timestamps.
    for autor in data['autores']:
        a = Autor(name=autor['name'], youtube=autor['youtube'], twitter=autor['twitter'], github=autor['github'], twitch=autor['twitch'])
        a.save()
        for video in autor['videos']:
            t = Timestamp(time=video['timestamp']['time'], data=video['timestamp']['data'])
            t.save()
            v = Video(url=video['url'], tags=video['tags'], autor_id=a.id, timestamp_id=t.id, title=video['title'])
            v.save()
