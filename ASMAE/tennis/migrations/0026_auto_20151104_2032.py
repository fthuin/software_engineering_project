# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0025_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtState',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='court',
            options={'verbose_name': 'Court', 'permissions': (('Court', 'Manage Court'),)},
        ),
        migrations.AlterModelOptions(
            name='extra',
            options={'verbose_name': 'Extra', 'permissions': (('Extra', 'Manage Extra'),)},
        ),
        migrations.AlterModelOptions(
            name='pair',
            options={'verbose_name': 'Paire', 'permissions': (('Pair', 'Manage Pair'),)},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'Participant', 'permissions': (('User', 'Manage User'), ('Droit', 'Donner droit'))},
        ),
        migrations.AlterModelOptions(
            name='tournoi',
            options={'verbose_name': 'Tournoi', 'permissions': (('TournoiDesFamilles', 'Manage tournoi des familles'), ('DoubleHommes', 'Manage double hommes'), ('DoubleFemmes', 'Manage double femmes'), ('DoubleMixte', 'Manage double mixte'))},
        ),
        migrations.AlterField(
            model_name='court',
            name='codepostal',
            field=models.CharField(max_length=10, verbose_name=b'Code postal'),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoDimanche',
            field=models.BooleanField(default=False, verbose_name=b'Dispo dimanche'),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoSamedi',
            field=models.BooleanField(default=False, verbose_name=b'Dispo samedi'),
        ),
        migrations.AlterField(
            model_name='court',
            name='etat',
            field=models.ForeignKey(verbose_name=b'Etat', to='tennis.CourtState'),
        ),
        migrations.AlterField(
            model_name='court',
            name='id',
            field=models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(max_length=30, verbose_name=b'Localit\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='court',
            name='matiere',
            field=models.CharField(max_length=30, verbose_name=b'Mati\xc3\xa8re'),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(max_length=10, verbose_name=b'Num\xc3\xa9ro'),
        ),
        migrations.AlterField(
            model_name='court',
            name='rue',
            field=models.CharField(max_length=100, verbose_name=b'Rue'),
        ),
        migrations.AlterField(
            model_name='court',
            name='user',
            field=models.ForeignKey(verbose_name=b'Utilisateur', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(default=False, verbose_name=b'Valid\xc3\xa9'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name=b'Confirmation'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='id',
            field=models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='pay',
            field=models.BooleanField(default=False, verbose_name=b'Paiement'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(related_name='user1', verbose_name=b'Utilisateur 1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(related_name='user2', verbose_name=b'Utilisateur 2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pair',
            name='valid',
            field=models.BooleanField(default=False, verbose_name=b'Validation'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='codepostal',
            field=models.CharField(max_length=10, verbose_name=b'Code postal'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='datenaissance',
            field=models.DateTimeField(null=True, verbose_name=b'Date de naissance'),
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
            field=models.CharField(max_length=30, null=True, verbose_name=b'T\xc3\xa9l\xc3\xa9phone'),
        ),
    ]
