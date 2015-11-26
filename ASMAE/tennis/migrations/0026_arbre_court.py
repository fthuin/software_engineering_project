# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0025_auto_20151126_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbre',
            name='court',
            field=models.ForeignKey(blank=True, to='tennis.Court', null=True),
        ),
    ]
