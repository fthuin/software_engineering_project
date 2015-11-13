# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0048_auto_20151113_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arbre',
            name='winner',
        ),
        migrations.AddField(
            model_name='arbre',
            name='label',
            field=models.TextField(null=True),
        ),
    ]
