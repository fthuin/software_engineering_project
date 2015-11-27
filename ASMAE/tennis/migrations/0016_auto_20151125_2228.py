# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0015_auto_20151125_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='used',
            field=models.BooleanField(default=False),
        ),
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
            field=models.BooleanField(default=False, verbose_name='Validé'),
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
            field=models.CharField(verbose_name='Téléphone', null=True, max_length=30, blank=True),
        ),
    ]
