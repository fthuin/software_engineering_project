# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0021_auto_20151125_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='used',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
