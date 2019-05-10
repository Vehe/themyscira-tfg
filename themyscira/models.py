from django.db import models
from django.contrib.postgres.fields import ArrayField
import random

# Crea la tabla de Autor la cual contiene información sobre los autores disponibles.
class Autor(models.Model):
    name = models.CharField(max_length=30)
    youtube = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    twitch = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Crea la tabla Timestamp, la cual contentrá los códigos de tiempo de n video.
class Timestamp(models.Model):
    time = ArrayField(models.CharField(max_length=30), blank=True)
    data = ArrayField(models.CharField(max_length=50), blank=True)

# Crea la tabla Video, la cual tiene información sobre este.
# Cada vídeo puede tener un único autor y un único timestamp asociado.
class Video(models.Model):
    url = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    title = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    timestamp = models.ForeignKey(Timestamp, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Crea la tabla Question, que tiene información sobre la pregunta que se realiza.
class Question(models.Model):
    title = models.CharField(max_length=200)
    data = models.CharField(max_length=1000)
    tags = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    notificacion_email = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    # Genera un número random del 1 al 6, se usa en el template para generar una imagen de usuario aleatoria.
    def generate_random(self):
        return str(random.randint(1,6))

    def __str__(self):
        return self.title

# Crea la tabla Response, esta puede estar asociada a una y solo una pregunta.
class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.CharField(max_length=1000)

    def __str__(self):
        return self.data

# Crea la tabla RequestAutor, se usa para almacenar los autores que los usuario mediante el formulario de contacto envían.
class RequestAutor(models.Model):
    name = models.CharField(max_length=30)
    youtube = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    twitch = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # Devuelve la URL de youtube en formato array.
    def get_yt(self):
        return self.youtube.split('/')

    # Devuelve la URL de twitter en formato array.
    def get_twitter(self):
        return self.twitter.split('/')

    # Devuelve la URL de twitch en formato array.
    def get_twitch(self):
        return self.twitch.split('/')

    # Devuelve la URL de github en formato array.
    def get_github(self):
        return self.github.split('/')

# Crea la tabla RequestVideo, donde se almacenan los videos que los usuarios envían mediante el form de contacto.
class RequestVideo(models.Model):
    url = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    title = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    timestamp_time = ArrayField(models.CharField(max_length=30), blank=True)
    timestamp_data = ArrayField(models.CharField(max_length=30), blank=True)

    def __str__(self):
        return self.title

    # Devuelve una string con todos los tag separados por coma.
    def get_tags(self):
        return ", ".join(map(str,self.tags))
