# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0029_auto_20151201_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='logactivity',
            name='target',
            field=models.CharField(default='undefined', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(max_length=30, verbose_name=b'Localit\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(max_length=10, verbose_name=b'Num\xc3\xa9ro'),
        ),
        migrations.AlterField(
            model_name='court',
            name='usedLastYear',
            field=models.BooleanField(default=False, verbose_name=b'V\xc3\xa9t\xc3\xa9ran'),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(default=False, verbose_name=b'Valid\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='isAccountActivated',
            field=models.BooleanField(default=True, verbose_name=b'Compte activ\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='localite',
            field=models.CharField(max_length=30, verbose_name=b'Localit\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='numero',
            field=models.CharField(max_length=10, verbose_name=b'Num\xc3\xa9ro'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='prenom',
            field=models.CharField(max_length=30, verbose_name=b'Pr\xc3\xa9nom'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='telephone',
            field=models.CharField(max_length=30, null=True, verbose_name=b'T\xc3\xa9l\xc3\xa9phone', blank=True),
        ),
        migrations.AlterField(
            model_name='poule',
            name='court',
            field=models.ForeignKey(verbose_name=b'Terrain', blank=True, to='tennis.Court', null=True),
        ),
        migrations.AlterField(
            model_name='poule',
            name='id',
            field=models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
    ]
