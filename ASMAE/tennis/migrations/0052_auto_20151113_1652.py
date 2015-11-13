# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0051_auto_20151113_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pair',
            name='group',
        ),
        migrations.AddField(
            model_name='poule',
            name='gagnant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='poule',
            name='perdant',
            field=models.BooleanField(default=False),
        ),
    ]
