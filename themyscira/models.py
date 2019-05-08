from django.db import models
from django.contrib.postgres.fields import ArrayField
import random

class Autor(models.Model):
    name = models.CharField(max_length=30)
    youtube = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    twitch = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Timestamp(models.Model):
    time = ArrayField(models.CharField(max_length=30), blank=True)
    data = ArrayField(models.CharField(max_length=50), blank=True)

class Video(models.Model):
    url = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    title = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    timestamp = models.ForeignKey(Timestamp, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=200)
    data = models.CharField(max_length=1000)
    tags = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    notificacion_email = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    def generate_random(self):
        return str(random.randint(1,6))

    def __str__(self):
        return self.title

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.CharField(max_length=1000)

    def __str__(self):
        return self.data

class RequestAutor(models.Model):
    name = models.CharField(max_length=30)
    youtube = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    twitch = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RequestVideo(models.Model):
    url = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    title = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    timestamp_time = ArrayField(models.CharField(max_length=30), blank=True)
    timestamp_data = ArrayField(models.CharField(max_length=30), blank=True)

    def __str__(self):
        return self.title
