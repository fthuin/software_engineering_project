# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0017_auto_20151125_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='nom',
            field=models.CharField(unique=True, max_length=15, blank=True),
        ),
    ]
