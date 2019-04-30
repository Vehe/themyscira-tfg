from themyscira.models import *
import json

# Creamos un nuevo autor y le asignamos sus datos
def createAutor(d):
    new_autor = Autor()
    new_autor.name = d['creator']['name']
    new_autor.youtube = d['creator']['youtube']
    new_autor.twitter = d['creator']['twitter']
    new_autor.github = d['creator']['github']
    new_autor.twitch = d['creator']['twitch']
    new_autor.save()
    return

# Crea una nueva entrada de video, junto a sus timestamps correspondientes
def uploadJSON(d, autor):
    new_timestamp = Timestamp()
    new_timestamp.time = d['timestamp']['time']
    new_timestamp.data = d['timestamp']['data']
    new_timestamp.save()

    new_video = Video()
    new_video.url = d['url']
    new_video.autor = Autor.objects.get(name=autor)
    new_video.timestamp = new_timestamp
    new_video.tags = d['tags']
    new_video.save()
    return

# Abrimos el fichero que contiene los diferentes JSON a introducir
with open('videos.json', 'r') as file:
    data = file.read().split('---')

# Por cada JSON, lo añade a la base de datos, comprobando que el video no se encuentra ya en esta
for j in data:
    new_json = json.loads(j.strip())
    a_name = new_json['creator']['name']
    if not Video.objects.filter(url=new_json['url']).exists():
        if not Autor.objects.filter(name=a_name).exists():
            createAutor(new_json)
        uploadJSON(new_json, a_name)
