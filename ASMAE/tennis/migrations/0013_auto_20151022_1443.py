# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0012_auto_20151022_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournoi',
            name='nom',
            field=models.CharField(max_length=50),
        ),
    ]
