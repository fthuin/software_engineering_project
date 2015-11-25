# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0010_auto_20151124_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tournoistatus',
            options={'verbose_name': 'Status des tournoi'},
        ),
    ]
