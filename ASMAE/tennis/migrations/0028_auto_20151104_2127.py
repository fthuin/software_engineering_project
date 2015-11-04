# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0027_auto_20151104_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='boite',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
