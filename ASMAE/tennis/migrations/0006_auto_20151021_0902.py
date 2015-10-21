# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0005_auto_20151020_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='prix',
            field=models.DecimalField(max_digits=2, decimal_places=2),
        ),
    ]
