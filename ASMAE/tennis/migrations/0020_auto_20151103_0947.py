# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0019_auto_20151103_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupe',
            name='court',
            field=models.ForeignKey(default=None, to='tennis.Court'),
        ),
    ]
