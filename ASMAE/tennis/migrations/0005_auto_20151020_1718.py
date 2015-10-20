# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0004_auto_20151019_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extra',
            name='user',
        ),
        migrations.AlterField(
            model_name='extra',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
