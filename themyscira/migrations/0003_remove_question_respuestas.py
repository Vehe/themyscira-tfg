# Generated by Django 2.2 on 2019-04-29 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('themyscira', '0002_question_response'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='respuestas',
        ),
    ]
