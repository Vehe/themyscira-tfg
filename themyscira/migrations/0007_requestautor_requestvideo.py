# Generated by Django 2.2 on 2019-05-08 12:26

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('themyscira', '0006_auto_20190502_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestAutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('youtube', models.CharField(max_length=100)),
                ('twitter', models.CharField(max_length=100)),
                ('github', models.CharField(max_length=100)),
                ('twitch', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RequestVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, size=None)),
                ('title', models.CharField(max_length=100)),
                ('timestamp_time', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, size=None)),
                ('timestamp_data', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, size=None)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='themyscira.Autor')),
            ],
        ),
    ]