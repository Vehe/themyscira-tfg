# Generated by Django 2.2 on 2019-05-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themyscira', '0003_remove_question_respuestas'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]