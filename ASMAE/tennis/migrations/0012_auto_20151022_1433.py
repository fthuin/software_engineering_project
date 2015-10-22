# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0011_auto_20151022_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('confirm', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=False)),
                ('pay', models.BooleanField(default=False)),
                ('extra1', models.ManyToManyField(to='tennis.Extra', related_name='extra1')),
                ('extra2', models.ManyToManyField(to='tennis.Extra', related_name='extra2')),
            ],
        ),
        migrations.CreateModel(
            name='Tournoi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pair',
            name='tournoi',
            field=models.ForeignKey(to='tennis.Tournoi'),
        ),
        migrations.AddField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user1'),
        ),
        migrations.AddField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user2'),
        ),
    ]
