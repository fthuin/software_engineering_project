# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0018_auto_20151028_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'permissions': (('makegroup', 'manage the group'),)},
        ),
    ]
