# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0013_auto_20151022_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='comment1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='comment2',
            field=models.TextField(null=True),
        ),
    ]
