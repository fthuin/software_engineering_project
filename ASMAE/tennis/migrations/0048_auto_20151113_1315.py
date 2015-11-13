# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0047_tournoistatus_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arbre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.TextField(null=True)),
                ('winner', models.ForeignKey(blank=True, to='tennis.Pair', null=True)),
            ],
            options={
                'verbose_name': 'Arbre',
            },
        ),
        migrations.CreateModel(
            name='PouleStatus',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=25, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Status de la poule',
            },
        ),
        migrations.AlterField(
            model_name='tournoistatus',
            name='nom',
            field=models.CharField(max_length=25, verbose_name='Nom'),
        ),
        migrations.AddField(
            model_name='poule',
            name='status',
            field=models.ForeignKey(blank=True, to='tennis.PouleStatus', null=True),
        ),
    ]
