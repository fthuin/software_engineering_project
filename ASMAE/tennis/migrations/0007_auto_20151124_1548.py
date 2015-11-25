# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0006_auto_20151124_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupe',
            name='court',
        ),
        migrations.RemoveField(
            model_name='groupe',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='groupe',
            name='tournoi',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='isGroupLeader',
        ),
        migrations.DeleteModel(
            name='Groupe',
        ),
    ]
