from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.OneToOneField(User)
	titre = models.CharField(max_length=5)
	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=30)
	adresse = models.CharField(max_length=100)
	numero = models.IntegerField()
	boite = models.IntegerField()
	codepostal = models.IntegerField()
	localite = models.CharField(max_length=30)
	telephone = models.IntegerField()
	gsm = models.IntegerField()
	datenaissance = models.DateTimeField()
	classement = models.CharField(max_length=10)
	oldparticipant = models.BooleanField()

	def __str__(self):
		return self.prenom + self.nom


