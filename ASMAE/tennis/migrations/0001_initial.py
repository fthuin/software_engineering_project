# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arbre',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('data', models.TextField(null=True)),
                ('label', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Arbre',
            },
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('rue', models.CharField(max_length=100, verbose_name=b'Rue')),
                ('numero', models.CharField(max_length=10, verbose_name=b'Num\xc3\xa9ro')),
                ('boite', models.CharField(max_length=10, null=True, blank=True)),
                ('codepostal', models.CharField(max_length=10, verbose_name=b'Code postal')),
                ('localite', models.CharField(max_length=30, verbose_name=b'Localit\xc3\xa9')),
                ('acces', models.TextField(null=True, blank=True)),
                ('dispoSamedi', models.BooleanField(default=False, verbose_name=b'Dispo samedi')),
                ('dispoDimanche', models.BooleanField(default=False, verbose_name=b'Dispo dimanche')),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('commentaireStaff', models.TextField(null=True, blank=True)),
                ('valide', models.BooleanField(default=False, verbose_name=b'Valid\xc3\xa9')),
            ],
            options={
                'verbose_name': 'Terrain',
                'permissions': (('Court', 'Manage Court'),),
            },
        ),
        migrations.CreateModel(
            name='CourtState',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True)),
            ],
            options={
                'verbose_name': 'Etat de court',
            },
        ),
        migrations.CreateModel(
            name='CourtSurface',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True)),
            ],
            options={
                'verbose_name': 'Surface de court',
            },
        ),
        migrations.CreateModel(
            name='CourtType',
            fields=[
                ('nom', models.CharField(max_length=25, serialize=False, verbose_name=b'Nom', primary_key=True)),
            ],
            options={
                'verbose_name': 'Type de court',
            },
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('prix', models.DecimalField(max_digits=11, decimal_places=2)),
                ('commentaires', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Extra',
                'permissions': (('Extra', 'Manage Extra'),),
            },
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gsize', models.IntegerField(null=True)),
                ('court', models.ForeignKey(default=None, to='tennis.Court')),
            ],
        ),
        migrations.CreateModel(
            name='LogActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('section', models.CharField(max_length=50)),
                ('details', models.CharField(max_length=200)),
                ('user', models.ForeignKey(verbose_name=b'Utilisateur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Log',
            },
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('comment1', models.TextField(null=True, blank=True)),
                ('comment2', models.TextField(null=True, blank=True)),
                ('confirm', models.BooleanField(default=False, verbose_name=b'Confirmation')),
                ('valid', models.BooleanField(default=False, verbose_name=b'Validation')),
                ('pay', models.BooleanField(default=False, verbose_name=b'Paiement')),
                ('gagnant', models.BooleanField(default=False)),
                ('finaliste', models.BooleanField(default=False)),
                ('extra1', models.ManyToManyField(related_name='extra1', to='tennis.Extra')),
                ('extra2', models.ManyToManyField(related_name='extra2', to='tennis.Extra')),
            ],
            options={
                'verbose_name': 'Paire',
                'permissions': (('Pair', 'Manage Pair'),),
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=5)),
                ('nom', models.CharField(max_length=30)),
                ('prenom', models.CharField(max_length=30, verbose_name=b'Pr\xc3\xa9nom')),
                ('rue', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10, verbose_name=b'Num\xc3\xa9ro')),
                ('boite', models.CharField(max_length=10, null=True, blank=True)),
                ('codepostal', models.CharField(max_length=10, verbose_name=b'Code postal')),
                ('localite', models.CharField(max_length=30, verbose_name=b'Localit\xc3\xa9')),
                ('telephone', models.CharField(max_length=30, null=True, verbose_name=b'T\xc3\xa9l\xc3\xa9phone', blank=True)),
                ('fax', models.CharField(max_length=30, null=True, blank=True)),
                ('gsm', models.CharField(max_length=30, null=True)),
                ('datenaissance', models.DateTimeField(null=True, verbose_name=b'Date de naissance')),
                ('classement', models.CharField(max_length=10, null=True, blank=True)),
                ('oldparticipant', models.BooleanField(default=False)),
                ('isGroupLeader', models.BooleanField(default=False)),
                ('isAccountActivated', models.BooleanField(default=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Participant',
                'permissions': (('User', 'Manage User'), ('Droit', 'Donner droit')),
            },
        ),
        migrations.CreateModel(
            name='Poule',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('court', models.ForeignKey(blank=True, to='tennis.Court', null=True)),
                ('leader', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('paires', models.ManyToManyField(to='tennis.Pair')),
            ],
            options={
                'verbose_name': 'Poule',
            },
        ),
        migrations.CreateModel(
            name='PouleStatus',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('nom', models.CharField(max_length=25, verbose_name=b'Nom')),
            ],
            options={
                'verbose_name': 'Status de la poule',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point1', models.IntegerField(null=True)),
                ('point2', models.IntegerField(null=True)),
                ('paire1', models.ForeignKey(related_name='paire1', verbose_name=b'Paire 1', to='tennis.Pair')),
                ('paire2', models.ForeignKey(related_name='paire2', verbose_name=b'Paire 2', to='tennis.Pair')),
            ],
        ),
        migrations.CreateModel(
            name='Tournoi',
            fields=[
                ('nom', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('description', models.TextField(null=True)),
                ('jour', models.CharField(max_length=50)),
                ('arbre', models.ForeignKey(blank=True, to='tennis.Arbre', null=True)),
            ],
            options={
                'verbose_name': 'Tournoi',
                'permissions': (('TournoiDesFamilles', 'Manage tournoi des familles'), ('DoubleHommes', 'Manage double hommes'), ('DoubleFemmes', 'Manage double femmes'), ('DoubleMixte', 'Manage double mixte')),
            },
        ),
        migrations.CreateModel(
            name='TournoiStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('numero', models.IntegerField(unique=True, null=True, verbose_name=b'ID')),
                ('nom', models.CharField(max_length=25, verbose_name=b'Nom')),
            ],
            options={
                'verbose_name': 'Status du tournoi',
            },
        ),
        migrations.CreateModel(
            name='UserInWaitOfActivation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dayOfRegistration', models.DateTimeField()),
                ('confirmation_key', models.CharField(max_length=100)),
                ('participant', models.OneToOneField(to='tennis.Participant')),
            ],
        ),
        migrations.AddField(
            model_name='tournoi',
            name='status',
            field=models.ForeignKey(blank=True, to='tennis.TournoiStatus', null=True),
        ),
        migrations.AddField(
            model_name='poule',
            name='score',
            field=models.ManyToManyField(to='tennis.Score', blank=True),
        ),
        migrations.AddField(
            model_name='poule',
            name='status',
            field=models.ForeignKey(blank=True, to='tennis.PouleStatus', null=True),
        ),
        migrations.AddField(
            model_name='poule',
            name='tournoi',
            field=models.ForeignKey(to='tennis.Tournoi'),
        ),
        migrations.AddField(
            model_name='pair',
            name='tournoi',
            field=models.ForeignKey(to='tennis.Tournoi'),
        ),
        migrations.AddField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(related_name='user1', verbose_name=b'Utilisateur 1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(related_name='user2', verbose_name=b'Utilisateur 2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupe',
            name='leader',
            field=models.ForeignKey(default=None, to='tennis.Pair'),
        ),
        migrations.AddField(
            model_name='groupe',
            name='tournoi',
            field=models.ForeignKey(default=None, to='tennis.Tournoi'),
        ),
        migrations.AddField(
            model_name='court',
            name='etat',
            field=models.ForeignKey(verbose_name=b'Etat', to='tennis.CourtState'),
        ),
        migrations.AddField(
            model_name='court',
            name='matiere',
            field=models.ForeignKey(verbose_name=b'Surface', to='tennis.CourtSurface'),
        ),
        migrations.AddField(
            model_name='court',
            name='type',
            field=models.ForeignKey(verbose_name=b'Type', to='tennis.CourtType'),
        ),
        migrations.AddField(
            model_name='court',
            name='user',
            field=models.ForeignKey(verbose_name=b'Utilisateur', to=settings.AUTH_USER_MODEL),
        ),
    ]
