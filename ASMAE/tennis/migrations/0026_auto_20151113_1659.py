# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0025_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('score', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='court',
            name='attribue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournoi',
            name='status',
            field=models.CharField(default=datetime.datetime(2015, 11, 13, 16, 59, 21, 281231), max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupe',
            name='court',
            field=models.OneToOneField(default=None, to='tennis.Court'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(default=None, blank=True, to='tennis.Groupe', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='court',
            field=models.ForeignKey(default=None, to='tennis.Court'),
        ),
        migrations.AddField(
            model_name='match',
            name='paire_gagnante',
            field=models.ForeignKey(related_name='paire_gagnante', to='tennis.Pair'),
        ),
        migrations.AddField(
            model_name='match',
            name='paire_perdante',
            field=models.ForeignKey(related_name='paire_perdante', to='tennis.Pair'),
        ),
    ]
