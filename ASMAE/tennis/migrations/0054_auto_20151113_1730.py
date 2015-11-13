# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0053_auto_20151113_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pair',
            old_name='perdant',
            new_name='finaliste',
        ),
    ]
