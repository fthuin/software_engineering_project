# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0023_remove_court_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='infotournoi',
            name='addr',
            field=models.TextField(default='Place des Carabiniers, 5, 1030 Bruxelles', verbose_name=b'Adresse du QG'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='infotournoi',
            name='edition',
            field=models.IntegerField(default=42),
            preserve_default=False,
        ),
    ]
