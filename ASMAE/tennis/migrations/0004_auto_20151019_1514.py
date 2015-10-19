# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0003_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='datenaissance',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='oldparticipant',
            field=models.BooleanField(default=False),
        ),
    ]
