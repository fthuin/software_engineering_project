# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0013_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='infoTournoi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('prix', models.DecimalField(verbose_name="Prix de l'inscription", decimal_places=2, max_digits=11)),
                ('date', models.DateTimeField(verbose_name='Date du tournoi')),
            ],
        ),
    ]
