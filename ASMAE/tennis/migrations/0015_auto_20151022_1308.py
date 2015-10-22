# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0014_auto_20151022_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournoi',
            name='id',
        ),
        migrations.AlterField(
            model_name='tournoi',
            name='nom',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
