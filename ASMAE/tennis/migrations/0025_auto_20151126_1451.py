# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0024_auto_20151126_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='infotournoi',
            name='latitude',
            field=models.DecimalField(default=b'50.8539751', verbose_name=b'Latitude', max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AddField(
            model_name='infotournoi',
            name='longitude',
            field=models.DecimalField(default=b'4.398054', verbose_name=b'Longitude', max_digits=19, decimal_places=10, blank=True),
        ),
    ]
