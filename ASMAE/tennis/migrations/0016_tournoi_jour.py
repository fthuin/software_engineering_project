# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0015_auto_20151022_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournoi',
            name='jour',
            field=models.CharField(default='samedi', max_length=50),
            preserve_default=False,
        ),
    ]
