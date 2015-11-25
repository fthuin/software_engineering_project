# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0011_auto_20151124_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournoi',
            name='arbre',
            field=models.ForeignKey(to='tennis.Arbre', null=True, blank=True),
        ),
    ]
