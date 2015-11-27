# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0008_auto_20151124_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poulestatus',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tournoistatus',
            name='id',
        ),
        migrations.AddField(
            model_name='poulestatus',
            name='numero',
            field=models.IntegerField(serialize=False, verbose_name='Numero', default=1, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournoistatus',
            name='numero',
            field=models.IntegerField(serialize=False, verbose_name='Numero', default=2, primary_key=True),
            preserve_default=False,
        ),
    ]
