# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0007_auto_20151124_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournoistatus',
            name='numero',
            field=models.IntegerField(unique=True, null=True, verbose_name='Numero'),
        ),
    ]
