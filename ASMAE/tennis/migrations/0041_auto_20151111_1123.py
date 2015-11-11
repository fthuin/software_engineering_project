# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0040_auto_20151110_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poule',
            name='court',
            field=models.ForeignKey(to='tennis.Court', null=True),
        ),
        migrations.AlterField(
            model_name='poule',
            name='leader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
