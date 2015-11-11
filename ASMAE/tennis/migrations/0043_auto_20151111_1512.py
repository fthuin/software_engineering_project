# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0042_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='court',
        ),
        migrations.RemoveField(
            model_name='match',
            name='paire_gagnante',
        ),
        migrations.RemoveField(
            model_name='match',
            name='paire_perdante',
        ),
        migrations.RemoveField(
            model_name='court',
            name='attribue',
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
            name='valide',
            field=models.BooleanField(default=False, verbose_name=b'Valid\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='court',
            field=models.ForeignKey(default=None, to='tennis.Court'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(default=None, to='tennis.Groupe', null=True),
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
            name='score',
            field=models.ManyToManyField(to='tennis.Score'),
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
