# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0038_auto_20151109_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('court', models.ForeignKey(to='tennis.Court')),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('paires', models.ManyToManyField(to='tennis.Pair')),
                ('tournoi', models.ForeignKey(to='tennis.Tournoi')),
            ],
        ),
    ]
