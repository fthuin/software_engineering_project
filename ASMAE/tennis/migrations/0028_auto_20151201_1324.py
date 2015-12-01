# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0027_auto_20151127_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gagnants_alt', models.TextField(null=True, blank=True)),
                ('finalistes_alt', models.TextField(null=True, blank=True)),
                ('finalistes', models.ManyToManyField(related_name='finalistes', verbose_name='finalistes', to=settings.AUTH_USER_MODEL)),
                ('gagnants', models.ManyToManyField(related_name='gagnants', verbose_name='gagnants', to=settings.AUTH_USER_MODEL)),
                ('tournoi', models.ForeignKey(to='tennis.Tournoi')),
            ],
        ),
        migrations.AlterField(
            model_name='court',
            name='latitude',
            field=models.DecimalField(decimal_places=6, verbose_name='Latitude', null=True, blank=True, max_digits=19),
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(max_length=30, verbose_name='Localité'),
        ),
        migrations.AlterField(
            model_name='court',
            name='longitude',
            field=models.DecimalField(decimal_places=6, verbose_name='Longitude', null=True, blank=True, max_digits=19),
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
            model_name='infotournoi',
            name='addr',
            field=models.TextField(verbose_name='Adresse du QG'),
        ),
        migrations.AlterField(
            model_name='infotournoi',
            name='latitude',
            field=models.DecimalField(decimal_places=10, default='50.8539751', verbose_name='Latitude', blank=True, max_digits=19),
        ),
        migrations.AlterField(
            model_name='infotournoi',
            name='longitude',
            field=models.DecimalField(decimal_places=10, default='4.398054', verbose_name='Longitude', blank=True, max_digits=19),
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
            field=models.CharField(max_length=30, verbose_name='Téléphone', null=True, blank=True),
        ),
    ]
