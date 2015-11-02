# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0020_auto_20151102_1521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='court',
            options={'permissions': (('Court', 'Manage Court'),)},
        ),
    ]
