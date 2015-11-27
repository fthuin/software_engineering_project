# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0026_arbre_court'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name=b'Latitude', max_digits=19, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name=b'Longitude', max_digits=19, decimal_places=6, blank=True),
        ),
    ]
