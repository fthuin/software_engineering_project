# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0009_auto_20151124_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poulestatus',
            options={'verbose_name': 'Status des poule'},
        ),
        migrations.AlterModelOptions(
            name='tournoistatus',
            options={'verbose_name': 'Status des tournois'},
        ),
    ]
