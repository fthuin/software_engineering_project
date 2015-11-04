# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0030_auto_20151104_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='acces',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='comment1',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='comment2',
            field=models.TextField(null=True, blank=True),
        ),
    ]
