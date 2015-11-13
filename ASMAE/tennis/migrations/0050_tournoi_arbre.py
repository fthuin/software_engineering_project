# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0049_auto_20151113_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournoi',
            name='arbre',
            field=models.OneToOneField(null=True, to='tennis.Arbre', blank=True),
        ),
    ]
