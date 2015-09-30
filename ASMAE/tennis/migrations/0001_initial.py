# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('titre', models.CharField(max_length=5)),
                ('nom', models.CharField(max_length=30)),
                ('prenom', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('boite', models.IntegerField()),
                ('codepostal', models.IntegerField()),
                ('localite', models.CharField(max_length=30)),
                ('telephone', models.IntegerField()),
                ('gsm', models.IntegerField()),
                ('datenaissance', models.DateTimeField()),
                ('classement', models.CharField(max_length=10)),
                ('oldparticipant', models.BooleanField()),
            ],
        ),
    ]
