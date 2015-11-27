# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0015_auto_20151125_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=15, blank=True)),
            ],
            options={
                'verbose_name': 'Classement',
            },
        ),
        migrations.AlterField(
            model_name='participant',
            name='classement',
            field=models.CharField(max_length=30),
        ),
    ]
