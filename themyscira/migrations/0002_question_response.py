# Generated by Django 2.2 on 2019-04-29 19:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('themyscira', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('data', models.CharField(max_length=1000)),
                ('respuestas', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), blank=True, size=None)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, size=None)),
                ('notificacion_email', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=1000)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='themyscira.Question')),
            ],
        ),
    ]
