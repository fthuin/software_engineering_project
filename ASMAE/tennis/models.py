from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.OneToOneField(User,null=True)
	titre = models.CharField(max_length=5)
	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=30)
	rue = models.CharField(max_length=100)
	numero = models.CharField(max_length=10)
	boite = models.CharField(max_length=10,null=True)
	codepostal = models.CharField(max_length=10)
	localite = models.CharField(max_length=30)
	telephone = models.CharField(max_length=30,null=True)
	fax = models.CharField(max_length=30,null=True)
	gsm = models.CharField(max_length=30,null=True)
	datenaissance = models.DateTimeField(null=True)
	classement = models.CharField(max_length=10,null=True)
	oldparticipant = models.BooleanField(default=False)

	def __str__(self):
		return self.prenom +" "+ self.nom

class Extra(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=30)
	prix = models.DecimalField(max_digits=11,decimal_places=2)
	commentaires = models.TextField(null=True)
	def __str__(self):
		return self.nom

class Court(models.Model):
	id = models.AutoField(primary_key=True)
	rue = models.CharField(max_length=100)
	numero = models.CharField(max_length=10)
	boite = models.CharField(max_length=10,null=True)
	codepostal = models.CharField(max_length=10)
	localite = models.CharField(max_length=30)
	acces = models.TextField(null=True)
	matiere = models.CharField(max_length=30)
	type = models.CharField(max_length=30)
	dispoSamedi = models.BooleanField(default=False)
	dispoDimanche = models.BooleanField(default=False)
	etat = models.CharField(max_length=30)
	commentaire = models.TextField(null=True)
	commentaireStaff = models.TextField(null=True)
	valide = models.BooleanField(default=False)
	user = models.ForeignKey(User)

	def __str__(self):
		return str(self.id) +" "+ self.rue

class Tournoi(models.Model):
	nom = models.CharField(max_length=30)
	description = models.TextField(null=True)

class Pair(models.Model):
	id = models.AutoField(primary_key=True)
	tournoi = models.ForeignKey(Tournoi)
	user1 = models.ForeignKey(User, related_name='user1')
	user2 = models.ForeignKey(User, related_name='user2')
	extra1 = models.ManyToManyField(Extra, related_name='extra1')
	extra2 = models.ManyToManyField(Extra, related_name='extra2')
	confirm = models.BooleanField(default=False)
	valid = models.BooleanField(default=False)
	pay = models.BooleanField(default=False)
	def __str__(self):
		return str(self.id) +" "+ tournoi+" : "+user1.username+" et "+user2.username

# TODO : Cyril needs Pair
# TODO : Cyril needs Courts
# TODO : Cyril needs Payment
# TODO : Cyril needs Groups (with group leader)