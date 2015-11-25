# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0003_auto_20151123_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournoiCategorie',
            fields=[
                ('nom', models.CharField(primary_key=True, serialize=False, max_length=50)),
                ('age_min_p1', models.IntegerField(null=True)),
                ('age_min_p2', models.IntegerField(null=True)),
                ('age_max_p1', models.IntegerField(null=True)),
                ('age_max_p2', models.IntegerField(null=True)),
                ('sexe_p1', models.BooleanField(default=True)),
                ('sexe_p2', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Catégorie Tournoi',
            },
        ),
        migrations.CreateModel(
            name='TournoiTitle',
            fields=[
                ('nom', models.CharField(primary_key=True, serialize=False, max_length=50)),
                ('description', models.TextField(null=True)),
                ('jour', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Titre Tournoi',
            },
        ),
        migrations.RemoveField(
            model_name='tournoi',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tournoi',
            name='jour',
        ),
        migrations.RemoveField(
            model_name='tournoi',
            name='nom',
        ),
        migrations.AddField(
            model_name='tournoi',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, default=1),
            preserve_default=False,
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
            field=models.CharField(verbose_name='Téléphone', blank=True, null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='tournoi',
            name='arbre',
            field=models.ForeignKey(to='tennis.Arbre', null=True),
        ),
        migrations.AlterField(
            model_name='tournoi',
            name='status',
            field=models.ForeignKey(to='tennis.TournoiStatus', null=True),
        ),
        migrations.AddField(
            model_name='tournoi',
            name='categorie',
            field=models.ForeignKey(to='tennis.TournoiCategorie', null=True),
        ),
        migrations.AddField(
            model_name='tournoi',
            name='titre',
            field=models.ForeignKey(to='tennis.TournoiTitle', null=True),
        ),
    ]
