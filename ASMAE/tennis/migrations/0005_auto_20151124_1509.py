# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0004_auto_20151124_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournoicategorie',
            name='sexe_p1',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='tournoicategorie',
            name='sexe_p2',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
