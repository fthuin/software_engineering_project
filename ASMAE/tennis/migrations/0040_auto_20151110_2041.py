# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0039_poule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('point1', models.IntegerField(null=True)),
                ('point2', models.IntegerField(null=True)),
                ('paire1', models.ForeignKey(to='tennis.Pair', related_name='paire1', verbose_name='Paire 1')),
                ('paire2', models.ForeignKey(to='tennis.Pair', related_name='paire2', verbose_name='Paire 2')),
            ],
        ),
        migrations.AlterModelOptions(
            name='poule',
            options={'verbose_name': 'Poule'},
        ),
        migrations.AddField(
            model_name='poule',
            name='score',
            field=models.ManyToManyField(null=True, to='tennis.Score'),
        ),
    ]
