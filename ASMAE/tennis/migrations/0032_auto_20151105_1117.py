# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0031_auto_20151104_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtType',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True)),
            ],
            options={
                'verbose_name': 'Type de court',
            },
        ),
        migrations.AlterField(
            model_name='court',
            name='type',
            field=models.ForeignKey(verbose_name=b'Type', to='tennis.CourtType'),
        ),
    ]
