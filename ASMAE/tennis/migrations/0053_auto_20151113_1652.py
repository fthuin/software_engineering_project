# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0052_auto_20151113_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poule',
            name='gagnant',
        ),
        migrations.RemoveField(
            model_name='poule',
            name='perdant',
        ),
        migrations.AddField(
            model_name='pair',
            name='gagnant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pair',
            name='perdant',
            field=models.BooleanField(default=False),
        ),
    ]
