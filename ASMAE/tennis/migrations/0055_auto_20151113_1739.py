# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0054_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='court',
        ),
        migrations.RemoveField(
            model_name='match',
            name='paire_gagnante',
        ),
        migrations.RemoveField(
            model_name='match',
            name='paire_perdante',
        ),
        migrations.RemoveField(
            model_name='court',
            name='attribue',
        ),
        migrations.AddField(
            model_name='tournoi',
            name='status',
            field=models.ForeignKey(blank=True, to='tennis.TournoiStatus', null=True),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='court',
            field=models.ForeignKey(default=None, to='tennis.Court'),
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
