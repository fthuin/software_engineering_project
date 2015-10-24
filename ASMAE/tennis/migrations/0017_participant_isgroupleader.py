# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0016_tournoi_jour'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='isGroupLeader',
            field=models.BooleanField(default=False),
        ),
    ]
