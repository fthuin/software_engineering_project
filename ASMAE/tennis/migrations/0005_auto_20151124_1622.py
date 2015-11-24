# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0004_auto_20151124_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='isClassementVerifier',
            new_name='isClassementVerified',
        ),
    ]
