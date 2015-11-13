# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0045_auto_20151112_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournoiStatus',
            fields=[
                ('nom', models.CharField(max_length=25, verbose_name='Nom', serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'Status du tournoi',
            },
        ),
        migrations.AlterField(
            model_name='tournoi',
            name='status',
            field=models.ForeignKey(blank=True, to='tennis.TournoiStatus', null=True),
        ),
    ]
