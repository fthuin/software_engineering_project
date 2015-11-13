# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0046_auto_20151113_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournoistatus',
            name='id',
            field=models.IntegerField(primary_key=True, verbose_name='ID', default=0, serialize=False),
            preserve_default=False,
        ),
    ]
