# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0010_auto_20151021_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='commentaireStaff',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='court',
            name='valide',
            field=models.BooleanField(default=False),
        ),
    ]
