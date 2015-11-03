# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0021_auto_20151102_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pair',
            options={'permissions': (('Pair', 'Manage Pair'),)},
        ),
        migrations.AlterModelOptions(
            name='tournoi',
            options={'permissions': (('TournoiDesFamilles', 'Manage tournoi des familles'), ('DoubleHommes', 'Manage double hommes'), ('DoubleFemmes', 'Manage double femmes'), ('DoubleMixte', 'Manage double mixte'))},
        ),
    ]
