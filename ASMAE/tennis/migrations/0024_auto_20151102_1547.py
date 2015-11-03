# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0023_auto_20151102_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'permissions': (('User', 'Manage User'), ('Droit', 'Donner droit'))},
        ),
    ]
