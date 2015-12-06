# -*- coding: utf-8 -*-
'''
Implémentation de tous les models, ce sont les objets stockés dans la base
de données. Chaque class correspond à une table dans la base de données.
'''
from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime


class Ranking(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Classement"


class Participant(models.Model):
    user = models.OneToOneField(User, null=True)
    titre = models.CharField(max_length=5)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30, verbose_name="Prénom")
    rue = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, verbose_name="Numéro")
    boite = models.CharField(max_length=10, null=True, blank=True)
    codepostal = models.CharField(max_length=10, verbose_name="Code postal")
    localite = models.CharField(max_length=30, verbose_name="Localité")
    latitude = models.DecimalField(
        max_digits=19, decimal_places=10, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(
        max_digits=19, decimal_places=10, null=True, blank=True, verbose_name="Longitude")
    telephone = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Téléphone")
    fax = models.CharField(max_length=30, null=True, blank=True)
    gsm = models.CharField(max_length=30, null=True)
    datenaissance = models.DateTimeField(
        null=True, verbose_name="Date de naissance")
    classement = models.ForeignKey(Ranking)
    oldparticipant = models.BooleanField(default=False)
    isClassementVerified = models.BooleanField(default=False)
    isAccountActivated = models.BooleanField(default=True, verbose_name="Compte activé")

    def __str__(self):
        return self.prenom + " " + self.nom

    def __unicode__(self):
        return u'' + self.prenom + " " + self.nom

    def codeName(self):
        return u'' + self.prenom + " " + self.nom + " (" + self.user.username + ")"

    def fullName(self):
        return u'' + self.titre + " " + self.prenom + " " + self.nom

    def smallName(self):
        return u'' + self.prenom[0:1].upper() + ". " + self.nom

    def limitName(self):
        nom = self.nom
        if len(self.nom) >= 16:
            nom = nom[0:14] + ".."
        return u'' + self.prenom[0:1].upper() + ". " + nom

    def getAdresse(self):
        return u"" + self.numero + " " + self.rue + ", " + self.codepostal + " " + self.localite

    def shortAdresse(self):
        return self.localite + " Belgium"

    # def __eq__(self, other):
    #	return self.username == other.user.username

    class Meta:
        verbose_name = "Participant"
        permissions = (
            ("User", "Manage User"),
            ("Droit", "Donner droit"),
        )


class UserInWaitOfActivation(models.Model):
    participant = models.OneToOneField(Participant, null=False)
    dayOfRegistration = models.DateTimeField(null=False)
    confirmation_key = models.CharField(max_length=100, null=False)

    def isStillValid(self):
        return self.dayOfRegistration + datetime.timedelta(weeks=1) > datetime.datetime.now()

    def isKeyValid(self, key):
        return key == self.confirmation_key


class Extra(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=30)
    prix = models.DecimalField(max_digits=11, decimal_places=2)
    commentaires = models.TextField(null=True)

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Extra"
        permissions = (
            ("Extra", "Manage Extra"),
        )


class CourtSurface(models.Model):
    nom = models.CharField(max_length=25, primary_key=True, verbose_name="Nom")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Surface de court"


class CourtState(models.Model):
    nom = models.CharField(max_length=25, primary_key=True, verbose_name="Nom")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Etat de court"


class CourtType(models.Model):
    nom = models.CharField(max_length=25, primary_key=True, verbose_name="Nom")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Type de court"


class Court(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    rue = models.CharField(max_length=100, verbose_name='Rue')
    numero = models.CharField(max_length=10, verbose_name='Numéro')
    boite = models.CharField(max_length=10, null=True, blank=True)
    codepostal = models.CharField(max_length=10, verbose_name='Code postal')
    localite = models.CharField(max_length=30, verbose_name='Localité')
    latitude = models.DecimalField(
        max_digits=19, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(
        max_digits=19, decimal_places=6, null=True, blank=True, verbose_name="Longitude")
    acces = models.TextField(null=True, blank=True)
    matiere = models.ForeignKey(CourtSurface, verbose_name='Surface')
    type = models.ForeignKey(CourtType, verbose_name='Type')
    dispoSamedi = models.BooleanField(
        default=False, verbose_name='Dispo samedi')
    dispoDimanche = models.BooleanField(
        default=False, verbose_name='Dispo dimanche')
    etat = models.ForeignKey(CourtState, verbose_name='Etat')
    commentaire = models.TextField(null=True, blank=True)
    commentaireStaff = models.TextField(null=True, blank=True)
    valide = models.BooleanField(default=False, verbose_name='Validé')
    user = models.ForeignKey(User, verbose_name='Utilisateur')
    usedLastYear = models.BooleanField(default=False, verbose_name='Vétéran')

    def __str__(self):
        return str(self.id) + " " + self.rue

    def __unicode__(self):
        return u'' + repr(self.id) + ' ' + self.rue

    def dispo(self):
        if self.dispoSamedi and self.dispoDimanche:
            return u'' + "Samedi et dimanche"
        elif self.dispoSamedi:
            return u'' + "Samedi"
        elif self.dispoDimanche:
            return u'' + "Dimanche"
        else:
            return u'' + " - "

    def getAdresse(self):
        return u"" + self.numero + " " + self.rue + ", " + self.codepostal + " " + self.localite

    def shortAdresse(self):
        return self.localite + " Belgium"

    class Meta:
        verbose_name = "Terrain"
        permissions = (
            ("Court", "Manage Court"),
        )


class TournoiStatus(models.Model):
    numero = models.IntegerField(verbose_name='Numero', primary_key=True)
    nom = models.CharField(max_length=25, verbose_name="Nom")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Status des tournoi"


class Arbre(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField(null=True)
    label = models.TextField(null=True)
    court = models.ForeignKey(Court, null=True, blank=True)

    def __str__(self):
        return "Arbre n " + str(self.id)

    def __unicode__(self):
        return u'' + "Arbre n " + repr(self.id)

    class Meta:
        verbose_name = "Arbre"


class TournoiTitle(models.Model):
    nom = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(null=True)
    jour = models.CharField(max_length=50)
    sexe_p1 = models.CharField(max_length=30, null=True)
    sexe_p2 = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.nom)

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Titre Tournoi"


class TournoiCategorie(models.Model):
    nom = models.CharField(max_length=50, primary_key=True)
    age_min_p1 = models.IntegerField(null=True)
    age_min_p2 = models.IntegerField(null=True)
    age_max_p1 = models.IntegerField(null=True)
    age_max_p2 = models.IntegerField(null=True)

    def __str__(self):
        return str(self.nom)

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Catégorie Tournoi"


class Tournoi(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.ForeignKey(TournoiTitle, null=True)
    categorie = models.ForeignKey(TournoiCategorie, null=True)
    status = models.ForeignKey(TournoiStatus, null=True)
    arbre = models.ForeignKey(Arbre, null=True, blank=True)

    def __str__(self):
        if(self.titre.nom == self.categorie.nom):
            return str(self.titre.nom)
        else:
            return str(self.titre.nom) + ": " + str(self.categorie.nom)

    def __unicode__(self):
        if(self.titre.nom == self.categorie.nom):
            return u'' + self.titre.nom
        else:
            return u'' + self.titre.nom + ": " + self.categorie.nom

    def nom(self):
        if(self.titre.nom == self.categorie.nom):
            return str(self.titre.nom)
        else:
            return str(self.titre.nom) + "_" + str(self.categorie.nom)

    class Meta:
        verbose_name = 'Tournoi'
        permissions = (
            ("TournoiDesFamilles", "Manage tournoi des familles"),
            ("DoubleHommes", "Manage double hommes"),
            ("DoubleFemmes", "Manage double femmes"),
            ("DoubleMixte", "Manage double mixte"),
        )


class Pair(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    tournoi = models.ForeignKey(Tournoi)
    user1 = models.ForeignKey(
        User, related_name='user1', verbose_name="Utilisateur 1")
    user2 = models.ForeignKey(
        User, related_name='user2', verbose_name="Utilisateur 2")
    extra1 = models.ManyToManyField(Extra, related_name='extra1', blank=True)
    extra2 = models.ManyToManyField(Extra, related_name='extra2', blank=True)
    comment1 = models.TextField(null=True, blank=True)
    comment2 = models.TextField(null=True, blank=True)
    confirm = models.BooleanField(default=False, verbose_name="Confirmation")
    valid = models.BooleanField(default=False, verbose_name="Validation")
    pay = models.BooleanField(default=False, verbose_name="Paiement")
    gagnant = models.BooleanField(default=False)
    finaliste = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + str(self.tournoi) + " : " + str(self.user1.username) + " et " + str(self.user2.username)

    class Meta:
        verbose_name = 'Paire'
        permissions = (
            ("Pair", "Manage Pair"),
        )


class PouleStatus(models.Model):
    numero = models.IntegerField(verbose_name='Numero', primary_key=True)
    nom = models.CharField(max_length=25, verbose_name="Nom")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return u'' + self.nom

    class Meta:
        verbose_name = "Status des poule"


class Score(models.Model):
    paire1 = models.ForeignKey(
        Pair, related_name='paire1', verbose_name="Paire 1")
    paire2 = models.ForeignKey(
        Pair, related_name='paire2', verbose_name="Paire 2")
    point1 = models.IntegerField(null=True)
    point2 = models.IntegerField(null=True)

    def __str__(self):
        return "Score " + str(self.paire1.id) + " vs " + str(self.paire2.id)

    def __unicode__(self):
        return u'' + "Score " + repr(self.paire1.id) + " vs " + repr(self.paire2.id)


class Poule(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    tournoi = models.ForeignKey(Tournoi)
    paires = models.ManyToManyField(Pair)
    leader = models.ForeignKey(User, null=True, blank=True)
    court = models.ForeignKey(Court, null=True, blank=True, verbose_name = "Terrain")
    score = models.ManyToManyField(Score, blank=True)
    status = models.ForeignKey(PouleStatus, null=True, blank=True)

    def __str__(self):
        return "Poule n " + str(self.id)

    def __unicode__(self):
        return u'' + "Poule n " + repr(self.id)

    class Meta:
        verbose_name = "Poule"


class LogActivity(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="Utilisateur")
    section = models.CharField(max_length=50)
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + self.section + self.details

    class Meta:
        verbose_name = "Log"


class Resultat(models.Model):
    id = models.AutoField(primary_key=True)
    tournoi = models.ForeignKey(Tournoi)
    gagnants = models.ManyToManyField(
        User, related_name='gagnants', verbose_name="gagnants")
    gagnants_alt = models.TextField(null=True, blank=True)
    finalistes = models.ManyToManyField(
        User, related_name='finalistes', verbose_name="finalistes")
    finalistes_alt = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Resultat du " + str(self.tournoi)

    def __unicode__(self):
        return u'' + "Resultat du " + repr(self.tournoi)


class infoTournoi(models.Model):
    prix = models.DecimalField(
        max_digits=11, decimal_places=2, verbose_name="Prix de l'inscription")
    date = models.DateTimeField(verbose_name="Date du tournoi")
    edition = models.IntegerField(primary_key=True)
    addr = models.TextField(verbose_name="Adresse du QG")
    latitude = models.DecimalField(
        max_digits=19, decimal_places=10, default="50.8539751", blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(
        max_digits=19, decimal_places=10, default="4.398054", blank=True, verbose_name="Longitude")
    resultats = models.ManyToManyField(Resultat)

    def __str__(self):
        return "Edition " + str(self.edition)

    def __unicode__(self):
        return u'' + "Edition " + repr(self.edition)
