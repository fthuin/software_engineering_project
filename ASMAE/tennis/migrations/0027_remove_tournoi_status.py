# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0026_auto_20151113_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournoi',
            name='status',
        ),
    ]
