# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0037_auto_20151108_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournoi',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(verbose_name='Localité', max_length=30),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(verbose_name='Numéro', max_length=10),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(verbose_name='Validé', default=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='localite',
            field=models.CharField(verbose_name='Localité', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='numero',
            field=models.CharField(verbose_name='Numéro', max_length=10),
        ),
        migrations.AlterField(
            model_name='participant',
            name='prenom',
            field=models.CharField(verbose_name='Prénom', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='telephone',
            field=models.CharField(verbose_name='Téléphone', max_length=30, null=True, blank=True),
        ),
    ]
