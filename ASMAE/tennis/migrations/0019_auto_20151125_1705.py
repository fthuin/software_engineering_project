# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0018_auto_20151125_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='classement',
            field=models.ForeignKey(to='tennis.Ranking'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='nom',
            field=models.CharField(unique=True, max_length=15),
        ),
    ]
