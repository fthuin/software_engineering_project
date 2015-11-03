# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0019_auto_20151102_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extra',
            options={'permissions': (('Extra', 'Manage Extra'),)},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={},
        ),
    ]
