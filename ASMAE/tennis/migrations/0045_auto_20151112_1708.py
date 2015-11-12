# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0044_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(max_length=30, verbose_name='Localité'),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(max_length=10, verbose_name='Numéro'),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(verbose_name='Validé', default=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='localite',
            field=models.CharField(max_length=30, verbose_name='Localité'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='numero',
            field=models.CharField(max_length=10, verbose_name='Numéro'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='prenom',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='telephone',
            field=models.CharField(null=True, max_length=30, verbose_name='Téléphone', blank=True),
        ),
        migrations.AlterField(
            model_name='poule',
            name='score',
            field=models.ManyToManyField(to='tennis.Score', blank=True),
        ),
    ]
