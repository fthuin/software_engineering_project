# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0026_auto_20151104_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtSurface',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True)),
            ],
            options={
                'verbose_name': 'Surface de court',
            },
        ),
        migrations.AlterModelOptions(
            name='courtstate',
            options={'verbose_name': 'Etat de court'},
        ),
        migrations.AlterField(
            model_name='court',
            name='matiere',
            field=models.ForeignKey(verbose_name=b'Surface', to='tennis.CourtSurface'),
        ),
        migrations.AlterField(
            model_name='courtstate',
            name='nom',
            field=models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True),
        ),
    ]
