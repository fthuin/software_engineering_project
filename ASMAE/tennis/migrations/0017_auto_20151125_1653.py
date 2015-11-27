# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0016_auto_20151125_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='classement',
            field=models.ForeignKey(blank=True, to='tennis.Ranking', null=True),
        ),
    ]
