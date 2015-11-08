# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0033_logactivity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logactivity',
            options={'verbose_name': 'Log'},
        ),
        migrations.AddField(
            model_name='participant',
            name='isAccountActivated',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='codepostal',
            field=models.CharField(max_length=10, verbose_name='Code postal'),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoDimanche',
            field=models.BooleanField(default=False, verbose_name='Dispo dimanche'),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoSamedi',
            field=models.BooleanField(default=False, verbose_name='Dispo samedi'),
        ),
        migrations.AlterField(
            model_name='court',
            name='etat',
            field=models.ForeignKey(to='tennis.CourtState', verbose_name='Etat'),
        ),
        migrations.AlterField(
            model_name='court',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(max_length=30, verbose_name='Localité'),
        ),
        migrations.AlterField(
            model_name='court',
            name='matiere',
            field=models.ForeignKey(to='tennis.CourtSurface', verbose_name='Surface'),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(max_length=10, verbose_name='Numéro'),
        ),
        migrations.AlterField(
            model_name='court',
            name='rue',
            field=models.CharField(max_length=100, verbose_name='Rue'),
        ),
        migrations.AlterField(
            model_name='court',
            name='type',
            field=models.ForeignKey(to='tennis.CourtType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='court',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(default=False, verbose_name='Validé'),
        ),
        migrations.AlterField(
            model_name='courtstate',
            name='nom',
            field=models.CharField(max_length=25, serialize=False, primary_key=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='courtsurface',
            name='nom',
            field=models.CharField(max_length=25, serialize=False, primary_key=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='courttype',
            name='nom',
            field=models.CharField(max_length=25, serialize=False, primary_key=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='logactivity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name='Confirmation'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='pay',
            field=models.BooleanField(default=False, verbose_name='Paiement'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(verbose_name='Utilisateur 1', to=settings.AUTH_USER_MODEL, related_name='user1'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(verbose_name='Utilisateur 2', to=settings.AUTH_USER_MODEL, related_name='user2'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='valid',
            field=models.BooleanField(default=False, verbose_name='Validation'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='codepostal',
            field=models.CharField(max_length=10, verbose_name='Code postal'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='datenaissance',
            field=models.DateTimeField(null=True, verbose_name='Date de naissance'),
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
            field=models.CharField(max_length=30, null=True, blank=True, verbose_name='Téléphone'),
        ),
    ]
