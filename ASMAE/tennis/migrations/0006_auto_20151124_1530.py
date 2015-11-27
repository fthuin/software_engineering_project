# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0005_auto_20151124_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournoicategorie',
            name='sexe_p1',
        ),
        migrations.RemoveField(
            model_name='tournoicategorie',
            name='sexe_p2',
        ),
        migrations.AddField(
            model_name='tournoititle',
            name='sexe_p1',
            field=models.CharField(null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='tournoititle',
            name='sexe_p2',
            field=models.CharField(null=True, max_length=30),
        ),
    ]
