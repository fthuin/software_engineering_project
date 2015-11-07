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
        migrations.AlterField(
            model_name='court',
            name='codepostal',
            field=models.CharField(verbose_name='Code postal', max_length=10),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoDimanche',
            field=models.BooleanField(verbose_name='Dispo dimanche', default=False),
        ),
        migrations.AlterField(
            model_name='court',
            name='dispoSamedi',
            field=models.BooleanField(verbose_name='Dispo samedi', default=False),
        ),
        migrations.AlterField(
            model_name='court',
            name='etat',
            field=models.ForeignKey(verbose_name='Etat', to='tennis.CourtState'),
        ),
        migrations.AlterField(
            model_name='court',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='court',
            name='localite',
            field=models.CharField(verbose_name='Localité', max_length=30),
        ),
        migrations.AlterField(
            model_name='court',
            name='matiere',
            field=models.ForeignKey(verbose_name='Surface', to='tennis.CourtSurface'),
        ),
        migrations.AlterField(
            model_name='court',
            name='numero',
            field=models.CharField(verbose_name='Numéro', max_length=10),
        ),
        migrations.AlterField(
            model_name='court',
            name='rue',
            field=models.CharField(verbose_name='Rue', max_length=100),
        ),
        migrations.AlterField(
            model_name='court',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='tennis.CourtType'),
        ),
        migrations.AlterField(
            model_name='court',
            name='user',
            field=models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='court',
            name='valide',
            field=models.BooleanField(verbose_name='Validé', default=False),
        ),
        migrations.AlterField(
            model_name='courtstate',
            name='nom',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Nom', max_length=25),
        ),
        migrations.AlterField(
            model_name='courtsurface',
            name='nom',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Nom', max_length=25),
        ),
        migrations.AlterField(
            model_name='courttype',
            name='nom',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Nom', max_length=25),
        ),
        migrations.AlterField(
            model_name='logactivity',
            name='user',
            field=models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pair',
            name='confirm',
            field=models.BooleanField(verbose_name='Confirmation', default=False),
        ),
        migrations.AlterField(
            model_name='pair',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='pay',
            field=models.BooleanField(verbose_name='Paiement', default=False),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user1', verbose_name='Utilisateur 1'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user2', verbose_name='Utilisateur 2'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='valid',
            field=models.BooleanField(verbose_name='Validation', default=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='codepostal',
            field=models.CharField(verbose_name='Code postal', max_length=10),
        ),
        migrations.AlterField(
            model_name='participant',
            name='datenaissance',
            field=models.DateTimeField(null=True, verbose_name='Date de naissance'),
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
            field=models.CharField(null=True, verbose_name='Téléphone', max_length=30, blank=True),
        ),
    ]
