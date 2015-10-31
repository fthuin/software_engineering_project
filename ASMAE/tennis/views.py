#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm
from tennis.models import Extra, Participant,Court, Tournoi, Pair
from tennis.mail import send_confirmation_email_court_registered, send_confirmation_email_pair_registered, send_email_start_tournament
import re, math
import datetime
from itertools import chain
from django.contrib.auth.decorators import permission_required

# Create your views here.
def home(request):
	return render(request,'tennis/home.html',locals())

def sponsors(request):
	return render(request,'tennis/sponsors.html',locals())

def contact(request):
	return render(request,'tennis/contact.html',locals())

def tournoi(request):
	if request.user.is_authenticated():
		nonComfirme = request.user.user1.filter(confirm=False)
		demande = request.user.user2.filter(confirm=False)
		inscrit1 = request.user.user1.filter(confirm=True)
		inscrit2 = request.user.user2.filter(confirm=True)
		inscrit =  list(chain(inscrit1,inscrit2))
		return render(request,'tennis/tournoi.html',locals())
	return redirect(reverse(home))

def inscriptionTournoi(request):
	Ex = Extra.objects.all()
	Tour = Tournoi.objects.all()
	Use = User.objects.all().order_by('username')

	for u in Use:
		bd = u.participant.datenaissance
		fb = bd.strftime('%d/%m/%Y')
		u.fb = fb

	if request.method == "POST":
		#On recupère les donnée du formualaire
		username2 = request.POST['username2']
		comment1 = request.POST['remarque']
		extra = request.POST.getlist('extra')
		#On recupere les extras pris par l'utilisateur
		extra1 = list()
		for elem in extra:
			extra1.append(Extra.objects.filter(id=elem)[0])
		#On en déduit les extras non pris par l'utilisateur
		extranot1 = list()
		Ex = Extra.objects.all()
		for elem in Ex:
			contained = False
			for el in extra1:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot1.append(Extra.objects.filter(id=elem.id)[0])

		#On recupere le tournoi(et on vérifie que l'utilisateur a bien entré un tournoi)
		nomTournoi = request.POST['tournoi']

		if (nomTournoi==""):
			errorAdd = "Veuillez selectionner un tournoi!"
			return render(request,'tennis/inscriptionTournoi.html',locals())

		tournois = Tournoi.objects.filter(nom=nomTournoi)[0]
		#On vérifie que l'utilisateur a bien rentré un deuxieme joueur
		if (username2==""):
			errorAdd = "Veuillez rajouter un deuxieme joueur pour votre pair"
			return render(request,'tennis/inscriptionTournoi.html',locals())

		#On véririe qu'il ne s'est pas entré lui meme
		user = User.objects.filter(username=request.user.username)[0]
		user2 = User.objects.filter(username=username2)[0]

		if (user==user2):
			errorAdd = "Vous ne pouvez pas faire une pair avec vous meme"
			return render(request,'tennis/inscriptionTournoi.html',locals())

		#Série de vérification pour que l'utilisateur ou son partenaire ne soit pas inscrit dans un tournoi du meme jour
		user1Tournoi1 = user.user1.all()
		user1Tournoi2 = user.user2.all()

		user2Tournoi1 = user2.user1.all()
		user2Tournoi2 = user2.user2.all()

		for elem in user1Tournoi1:
			if(elem.tournoi.jour == tournois.jour):
				errorAdd = "Vous etes deja inscrit a un tournoi ce jour!"
				return render(request,'tennis/inscriptionTournoi.html',locals())

		for elem in user1Tournoi2:
			if(elem.tournoi.jour == tournois.jour):
				errorAdd = "Vous etes deja inscrit a un tournoi ce jour!"
				return render(request,'tennis/inscriptionTournoi.html',locals())

		for elem in user2Tournoi1:
			if(elem.tournoi.jour == tournois.jour and elem.confirm):
				errorAdd = "Le joueur 2 est deja inscrit dans un tournoi ce jour!"
				return render(request,'tennis/inscriptionTournoi.html',locals())

		for elem in user2Tournoi2:
			if(elem.tournoi.jour == tournois.jour and elem.confirm):
				errorAdd = "Le joueur 2 est deja inscrit dans un tournoi ce jour!"
				return render(request,'tennis/inscriptionTournoi.html',locals())

		#On cré la pair
		pair = Pair(tournoi = tournois,user1=user,user2=user2,comment1 = comment1,confirm = False,valid = False,pay = False)
		pair.save()
		#On rajoute les extras
		for elem in extra:
			ext = Extra.objects.filter(id=elem)[0]
			pair.extra1.add(ext)

		# Send mail
		#send_confirmation_email_pair_registered(Participant.objects.get(user=pair.user1), Participant.objects.get(user=pair.user2))

		pair.save()
		return redirect(reverse(tournoi))

	if request.user.is_authenticated():
		extranot1 = Extra.objects.all()

		return render(request,'tennis/inscriptionTournoi.html',locals())
	return redirect(reverse(home))

def confirmPair(request,id):
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.filter(id=id)[0]
	if pair.user2 != request.user:
		return redirect(reverse(tournoi))
	if request.method == "POST":
		if request.POST['action'] == "validate":
			remarque = request.POST['remarque']
			extra = request.POST.getlist('extra')
			print(extra)


			pair.confirm = True
			pair.comment2 = remarque
			pair.save()

			for elem in extra:
				ext = Extra.objects.filter(id=elem)[0]
				pair.extra2.add(ext)

			pair.save()


			return redirect(reverse(tournoi))
		if request.POST['action'] == "refuse":

			pair.delete()
			return redirect(reverse(tournoi))
			#TODO Envoyer mail a l'user 1 pour lui dire que son pote veut pas de lui
	if request.user.is_authenticated():
		#TODO check si il peut confirmer cette pair

		extra1 = pair.extra1.all()
		extranot1 = list()
		Ex = Extra.objects.all()
		for elem in Ex:
			contained = False
			for el in extra1:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot1.append(Extra.objects.filter(id=elem.id)[0])




		return render(request,'tennis/confirmPair.html',locals())
	return redirect(reverse(home))

def cancelPair(request,id):
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.filter(id=id)[0]
	if pair.user1 != request.user:
		return redirect(reverse(tournoi))
	if request.method == "POST":
		#TODO check si il peut annuler cette pair
		pair.delete()
		return redirect(reverse(tournoi))
	if request.user.is_authenticated():

		extra1 = pair.extra1.all()
		Ex = Extra.objects.all()
		extranot1 = list()
		for elem in Ex:
			contained = False
			for el in extra1:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot1.append(Extra.objects.filter(id=elem.id)[0])

		return render(request,'tennis/cancelPair.html',locals())
	return redirect(reverse(home))

def viewPair(request,id):
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.filter(id=id)[0]
	if pair.user1 != request.user and pair.user2 != request.user:
		return redirect(reverse(tournoi))
	if request.user.is_authenticated():


		Ex = Extra.objects.all()
		extra1 = pair.extra1.all()
		extranot1 = list()
		for elem in Ex:
			contained = False
			for el in extra1:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot1.append(Extra.objects.filter(id=elem.id)[0])

		extra2 = pair.extra2.all()
		extranot2 = list()
		for elem in Ex:
			contained = False
			for el in extra2:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot2.append(Extra.objects.filter(id=elem.id)[0])


		return render(request,'tennis/viewPair.html',locals())
	return redirect(reverse(home))

def payPair(request,id):
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.filter(id=id)[0]
	if pair.user1 != request.user and pair.user2 != request.user:
		return redirect(reverse(tournoi))
	if request.user.is_authenticated():
		#TODO check si il peut payer cette pair
		Ex = Extra.objects.all()
		extra1 = pair.extra1.all()
		extra2 = pair.extra2.all()
		extraa = extra1 | extra2
		extraa.order_by('nom')
		totalprice = 40.00
		extraList = list()
		currentItem = extraa[0]
		count = 0
		for extra in extraa:
			if currentItem.id == extra.id:
				count = count+1
			else:
				extraList.append((currentItem.nom,currentItem.prix,count))
				totalprice = totalprice + float((count*currentItem.prix))
				currentItem = extra
				count = 1
		extraList.append((currentItem.nom,currentItem.prix,count))
		totalprice = totalprice + float((count*currentItem.prix))


		return render(request,'tennis/payPair.html',locals())
	return redirect(reverse(home))

def terrain(request):
	if request.user.is_authenticated():
		court = Court.objects.filter(user=request.user)
		return render(request,'tennis/terrain.html',locals())
	return redirect(reverse(home))

def registerTerrain(request):
	if request.method == "POST":
		rue = request.POST['rue']
		numero = request.POST['numero']
		boite = request.POST['boite']
		postalcode = request.POST['postalcode']
		locality = request.POST['loclity']
		acces = request.POST['acces']
		matiere = request.POST['matiere']
		type = request.POST['type']
		etat = request.POST['etat']
		commentaire = request.POST['comment']
		if request.POST.__contains__("dispoSamedi"):
				dispoSamedi = True
		else:
			dispoSamedi = False
		if request.POST.__contains__("dispoDimanche"):
				dispoDimanche = True
		else:
			dispoDimanche = False

		if (rue=="" or numero=="" or postalcode=="" or locality=="" or matiere=="" or type=="" or etat==""):
			errorAdd = "Veuillez remplir tous les champs obligatoires !"
			return render(request,'tennis/registerTerrain.html',locals())

		# Create court object
		court = Court(rue = rue,numero=numero,boite=boite,codepostal=postalcode,localite=locality,acces=acces,matiere=matiere,type=type,dispoDimanche=dispoDimanche,dispoSamedi=dispoSamedi,etat= etat,commentaire=commentaire,user = request.user)

		# Send confirmation mail
		##send_confirmation_email_court_registered(Participant.objects.get(user=request.user), court)

		court.save()

		return redirect(reverse(terrain))

	if request.user.is_authenticated():
		return render(request,'tennis/registerTerrain.html',locals())
	return redirect(reverse(home))

def editTerrain(request,id):
	court = Court.objects.filter(id=id)

	if len(court) <1:
		return redirect(reverse(terrain))
	court = Court.objects.filter(id=id)[0]
	if court.user != request.user:
		return redirect(reverse(terrain))

	if request.method == "POST":
		if request.POST['action'] == "modifyCourt":
			rue = request.POST['rue']
			numero = request.POST['numero']
			boite = request.POST['boite']
			postalcode = request.POST['postalcode']
			locality = request.POST['loclity']
			acces = request.POST['acces']
			matiere = request.POST['matiere']
			type = request.POST['type']
			etat = request.POST['etat']
			commentaire = request.POST['comment']
			if request.POST.__contains__("dispoSamedi"):
					dispoSamedi = True
			else:
				dispoSamedi = False
			if request.POST.__contains__("dispoDimanche"):
					dispoDimanche = True
			else:
				dispoDimanche = False


			if (rue=="" or numero=="" or postalcode=="" or locality=="" or matiere=="" or type=="" or etat==""):
				errorAdd = "Veuillez remplir tous les champs obligatoires !"
				return render(request,'tennis/registerTerrain.html',locals())


			court.rue = rue
			court.numero=numero
			court.boite=boite
			court.codepostal=postalcode
			court.localite=locality
			court.acces=acces
			court.matiere=matiere
			court.type=type
			court.dispoDimanche=dispoDimanche
			court.dispoSamedi=dispoSamedi
			court.etat= etat
			court.commentaire=commentaire
			court.user = request.user
			court.save()
			successEdit = "Terrain "+str(id)+" bien édité!"
			return redirect(reverse(terrain))

		if request.POST['action'] == "deleteCourt":

			court.delete()
			return redirect(reverse(terrain))

	if request.user.is_authenticated():

		if request.user == court.user:
			return render(request,'tennis/editTerrain.html',locals())
	return redirect(reverse(home))

def staff(request):
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/staff.html',locals())
	return redirect(reverse(home))

def staffTournoi(request):
	if request.method == "POST":
		if request.POST['action'] == "sendTournamentDataByMail":
				send_email_start_tournament() #TODO to change and link to a tournament
				successSend = "Les mails ont bien été envoyé"
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			allTournois = Tournoi.objects.all()
			allPairs = Pair.objects.all()
			allCourts = Court.objects.all()
			return render(request,'tennis/staffTournoi.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def staffTerrain(request):
	#List of Court
	allCourt = Court.objects.all()
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/staffTerrain.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def staffPaire(request):
	#List of Pair
	allPair = Pair.objects.all()
	Tour = Tournoi.objects.all()
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/staffPair.html',locals())
	return redirect(reverse(home))
@permission_required('tennis.Extra')
def staffExtra(request):
	if request.user.is_staff: #TODO
		Ex = Extra.objects.all()
		if request.method == "POST":
			if request.POST['action'] == "addExtra":
				nom = request.POST['name']
				prix = request.POST['price']
				message = request.POST['message']

				if nom=="":
					errorAdd = "Veuillez rajouter un nom à l'extra!"
					return render(request,'tennis/staffExtra.html',locals())

				if not is_number(prix):
					errorAdd = "Le prix n'a pas le bon format"
					return render(request,'tennis/staffExtra.html',locals())

				extra = Extra(nom=nom,prix=prix,commentaires = message)
				extra.save()

				successAdd = "Extra bien ajouté!"

			if request.POST['action'] == "modifyExtra":
				id = request.POST['id']
				nom = request.POST['name']
				prix = request.POST['price']
				message = request.POST['message']

				extra = Extra.objects.filter(id = id)[0]

				if nom=="":
					errorEdit = "Veuillez rajouter un nom à l'extra!"
					return render(request,'tennis/staffExtra.html',locals())

				if not is_number(prix):
					errorEdit = "Le prix n'a pas le bon format"
					return render(request,'tennis/staffExtra.html',locals())


				extra.nom = nom
				extra.prix = prix
				extra.commentaires = message
				extra.save()
				successEdit = "Extra bien édité!"

			if request.POST['action'] == "deleteExtra":
				id = request.POST['id']
				extra = Extra.objects.filter(id = id)[0]
				extra.delete()
				successDelete = "Extra bien supprimé!"

		if request.user.is_authenticated():
			return render(request,'tennis/staffExtra.html',locals())
	return redirect(reverse(home))

#TODO permission droit
def staffPerm(request):
	Use = User.objects.all().order_by('username')
	tournoiAll = Tournoi.objects.all()
	for u in Use:
		bd = u.participant.datenaissance
		fb = bd.strftime('%d/%m/%Y')
		u.fb = fb
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/staffPerm.html',locals())
	return redirect(reverse(home))

@permission_required('auth.User')
def staffUser(request):
	Use = User.objects.all().order_by('username')
	for u in Use:
		bd = u.participant.datenaissance
		fb = bd.strftime('%d/%m/%Y')
		u.fb = fb
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/staffUser.html',locals())
	return redirect(reverse(home))

@permission_required('auth.User')
def viewUser(request,name):

	use = User.objects.filter(username=name)

	if len(use) <1:
		return redirect(reverse(staffUser))

	use = use[0]

	birthdate = use.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	terrain = Court.objects.filter(user=use)
	tournoi1 = Pair.objects.filter(user1=use,confirm=True)
	tournoi2 = Pair.objects.filter(user2=use,confirm=True)
	tournoi = list(chain(tournoi1, tournoi2))
	if request.user.is_authenticated():
		if request.user.is_staff: #TODO
			return render(request,'tennis/viewUser.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def validateTerrain(request, id):
	if request.user.is_staff:
		court = Court.objects.filter(id=id)[0]
		if request.method == "POST":
			message = request.POST['message']
			if request.POST.__contains__("valide"):
				valide = True
			else:
				valide = False

			court.commentaireStaff = message
			court.valide = valide
			court.save()
			successEdit = "Terrain bien édité!"

		if request.user.is_authenticated():
			return render(request,'tennis/validateTerrain.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def editTerrainStaff(request, id):
	if request.user.is_staff:
		court = Court.objects.filter(id=id)[0]
		if request.method == "POST":
			if request.POST['action'] == "modifyCourt":
				rue = request.POST['rue']
				numero = request.POST['numero']
				boite = request.POST['boite']
				postalcode = request.POST['postalcode']
				locality = request.POST['loclity']
				acces = request.POST['acces']
				matiere = request.POST['matiere']
				type = request.POST['type']
				etat = request.POST['etat']
				commentaire = request.POST['comment']
				if request.POST.__contains__("dispoSamedi"):
						dispoSamedi = True
				else:
					dispoSamedi = False
				if request.POST.__contains__("dispoDimanche"):
						dispoDimanche = True
				else:
					dispoDimanche = False


				if (rue=="" or numero=="" or postalcode=="" or locality=="" or matiere=="" or type=="" or etat==""):
					errorAdd = "Veuillez remplir tous les champs obligatoires !"
					return render(request,'tennis/registerTerrain.html',locals())


				court.rue = rue
				court.numero=numero
				court.boite=boite
				court.codepostal=postalcode
				court.localite=locality
				court.acces=acces
				court.matiere=matiere
				court.type=type
				court.dispoDimanche=dispoDimanche
				court.dispoSamedi=dispoSamedi
				court.etat= etat
				court.commentaire=commentaire
				court.user = request.user
				court.save()
				#successEdit = "Terrain "+str(id)+" bien édité!"
				return redirect(reverse(validateTerrain,args={id}))

			if request.POST['action'] == "deleteCourt":
				#TODO delete terrain staff
				court.delete()
				return redirect(reverse(staffTerrain))
		if request.user.is_authenticated():
			return render(request,'tennis/editTerrainStaff.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def validatePair(request, id):
	if request.user.is_staff:
		pair = Pair.objects.filter(id=id)[0]
		if request.method == "POST":
			if request.POST['action'] == "editPair":
				valid = request.POST['valid']
				paid = request.POST['pay']
				if valid == "Oui":
					valider = True
				else:
					valider = False
				if paid == "Oui":
					payer = True
				else:
					payer = False
				pair.valid = valider
				pair.pay = payer
				pair.save()

				return redirect(reverse(staffPaire))

			if request.POST['action'] == "deletePair":
				pair.delete()
				return redirect(reverse(staffPaire))


		Ex = Extra.objects.all()
		extra1 = pair.extra1.all()
		extranot1 = list()
		for elem in Ex:
			contained = False
			for el in extra1:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot1.append(Extra.objects.filter(id=elem.id)[0])

		extra2 = pair.extra2.all()
		extranot2 = list()
		for elem in Ex:
			contained = False
			for el in extra2:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot2.append(Extra.objects.filter(id=elem.id)[0])

		birthdate1 = pair.user1.participant.datenaissance
		formatedBirthdate1 = birthdate1.strftime('%d/%m/%Y')
		birthdate2 = pair.user2.participant.datenaissance
		formatedBirthdate2 = birthdate2.strftime('%d/%m/%Y')
		if request.user.is_authenticated():
			return render(request,'tennis/validatePair.html',locals())
	return redirect(reverse(home))

def profil(request):
	birthdate = request.user.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	if request.method == "POST":
		if request.POST['action'] == 'updatePassword':


			password1 = request.POST['password1']
			password2 = request.POST['password2']

			#On vérifie que les password sont les memes
			if password1 != password2:
				errorMDP = "Les mots de passes sont différents !"
				return render(request,'tennis/profil.html',locals())

			#On vérifie la longeur du password
			if(len(password1) < 2):
				errorMDP = "Votre mot de passe doit contenir au moins 3 caractères"
				return render(request,'tennis/profil.html',locals())

			request.user.set_password(password1)
			request.user.save()
			successMDP = "Le mot de passe a bien été changé"
			user2 = authenticate(username=request.user, password=password1)
			login(request, user2)
			return render(request,'tennis/profil.html',locals())

		if request.POST['action'] == 'editProfil':

			firstname = request.POST['firstname']
			lastname = request.POST['lastname']
			gsm = request.POST['gsm']
			tel = request.POST['tel']
			fax = request.POST['fax']
			title = request.POST['title']
			boite = request.POST['boite']
			street = request.POST['street']
			number = request.POST['number']
			locality = request.POST['locality']
			postalcode = request.POST['postalcode']
			birthdate = request.POST['birthdate']
			classement = request.POST['classement']

			if request.POST.__contains__("participated"):
				oldparticipant = True
			else:
				oldparticipant = False

			#check champs
			if (firstname=="" or lastname=="" or (tel==""
			and gsm=="") or street=="" or number=="" or locality=="" or postalcode=="" or birthdate==""):
				errorEdit = "Veuillez remplir tous les champs obligatoires !"
				return render(request,'tennis/profil.html',locals())

			#check format date
			if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$",birthdate) is None:
				errorEdit = "La date de naissance n'a pas le bon format"
				return render(request,'tennis/profil.html',locals())

			#On formate la date
			birthdate2 = birthdate.split("/")
			datenaissance = datetime.datetime(int(birthdate2[2]),int(birthdate2[1]),int(birthdate2[0]))

			participant = request.user.participant
			participant.titre = title
			participant.nom = lastname
			participant.prenom = firstname
			participant.rue = street
			participant.numero = number
			participant.boite = boite
			participant.codepostal = postalcode
			participant.localite = locality
			participant.telephone = tel
			participant.fax = fax
			participant.gsm = gsm
			participant.datenaissance = datenaissance
			participant.classement = classement
			participant.oldparticipant = oldparticipant
			participant.save()



			successEdit = "Le profil a bien été changé"



			return render(request,'tennis/profil.html',locals())

	if request.user.is_authenticated():

		return render(request,'tennis/profil.html',locals())
	return redirect(reverse(home))




def connect(request):
	if request.method == "POST":
		#Recuperation des donnees
		username = request.POST['username']
		password = request.POST['password']

		#check email
		if username=="":
			error = "Veuillez entrer un nom d'utilisateur valide !"
			return render(request,'tennis/login.html',locals())

		#check password
		if password=="":
			error = "Veuillez entrer un mot de passe !"
			return render(request,'tennis/login.html',locals())

		#Connection
		user = authenticate(username=username, password=password)
		#Si l'utilisateur existe et qu'il est actif on le connecte sinon on affiche un message d'erreur
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(reverse(tournoi))
			else:
				error="Ce compte a été désactivé !"
				return render(request,'tennis/login.html',locals())
		else:
			#invalide login
			error = "Nom d'utilisateur ou mot de passe non conforme !"
			return render(request,'tennis/login.html',locals())
	if request.user.is_authenticated():
		return redirect(reverse(tournoi))
	return render(request,'tennis/login.html',locals())

def deconnect(request):
	logout(request)
	return redirect(reverse(home))

def username_present(username):
	if User.objects.filter(username=username).exists():
		return True

	return False

def email_present(email):
	if User.objects.filter(email=email).exists():
		return True

	return False

def register(request):
	if request.method == "POST":
		#Recuperation des donnees
		username = request.POST['username']
		password = request.POST['password']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		email = request.POST['email']
		gsm = request.POST['gsm']
		tel = request.POST['tel']
		fax = request.POST['fax']
		title = request.POST['title']
		boite = request.POST['boite']
		street = request.POST['street']
		number = request.POST['number']
		locality = request.POST['locality']
		postalcode = request.POST['postalcode']
		birthdate = request.POST['birthdate']
		classement = request.POST['classement']

		if request.POST.__contains__("participated"):
			oldparticipant = True
		else:
			oldparticipant = False



		#check champs
		if (username=="" or password=="" or firstname=="" or lastname=="" or email=="" or (tel==""
		and gsm=="") or street=="" or number=="" or locality=="" or postalcode=="" or birthdate==""):
			error = "Veuillez remplir tous les champs obligatoires !"
			return render(request,'tennis/register.html',locals())

		#Check username et email already taken
		if(username_present(username)):
			error = "Ce nom d'utilisateur n'est plus disponible !"
			return render(request,'tennis/register.html',locals())

		#On vérifie si l'email est deja dans la db
		if(email_present(email)):
			error = "Un compte avec cette addresse email existe déjà !"
			return render(request,'tennis/register.html',locals())

		#check username length
		if(len(username) < 2):
			error = "Votre nom d'utilisateur doit contenir au moins 3 caractères"
			return render(request,'tennis/register.html',locals())

		#check password length
		if(len(password) < 2):
			error = "Votre mot de passe doit contenir au moins 3 caractères"
			return render(request,'tennis/register.html',locals())

		#check format date
		if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$",birthdate) is None:
			error = "La date de naissance n'a pas le bon format"
			return render(request,'tennis/register.html',locals())

		#On format la date
		birthdate2 = birthdate.split("/")
		datenaissance = datetime.datetime(int(birthdate2[2]),int(birthdate2[1]),int(birthdate2[0]))

		#TODO : send email with code to finish registration and validate account

		#Account creation & redirect
		user = User.objects.create_user(username,email,password)
		user.save()
		participant = Participant(user = user,titre=title,nom=lastname,prenom=firstname,rue=street,numero=number,boite=boite,codepostal=postalcode,localite=locality,telephone=tel,fax=fax,gsm=gsm,classement = classement,oldparticipant = oldparticipant,datenaissance = datenaissance).save()

		#On connecte l'utilisateur
		user2 = authenticate(username=username, password=password)
		login(request, user2)
		return redirect(reverse(tournoi))

	if request.user.is_authenticated():
		return redirect(reverse(tournoi))
	return render(request,'tennis/register.html',locals())


def group(request):
	return render(request,'tennis/group.html',locals())

def recover(request):
	return render(request,'tennis/recover.html',locals())

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

