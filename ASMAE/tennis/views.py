#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm
from tennis.models import Extra, Participant,Court, Tournoi, Pair, CourtState, CourtSurface, CourtType,LogActivity, UserInWaitOfActivation, Poule,Score, PouleStatus,Arbre, TournoiStatus, TournoiTitle, TournoiCategorie, infoTournoi, Ranking, Resultat
from tennis.mail import send_confirmation_email_court_registered, send_confirmation_email_pair_registered, send_email_start_tournament, send_register_confirmation_email, test_send_mail
from tennis.classement import validate_classement_thread
import re, math, copy
import json
import datetime
from datetime import date, timedelta
from itertools import chain
from django.contrib.auth.decorators import permission_required,  user_passes_test
from django.contrib.auth.models import Permission,Group
from django.utils.crypto import get_random_string
from django.http import HttpResponse, HttpResponseRedirect
from tennis.pdfdocument import PDFTerrain, PDFPair, PDFPoule
from django.template.defaulttags import register
from django.db.models import Q
from functools import reduce
from operator import and_, or_

# Create your views here.
def home(request):
	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	edition = info.edition
	last = edition - 1
	date = info.date
	year = date.year
	month = date.month
	month_text = ""
	if month == 1:
		month_text = "janvier"
	elif month == 2:
		month_text = "février"
	elif month == 3:
		month_text = "mars"
	elif month == 4:
		month_text = "avril"
	elif month == 5:
		month_text = "mai"
	elif month == 6:
		month_text = "juin"
	elif month == 7:
		month_text = "juillet"
	elif month == 8:
		month_text = "août"
	elif month == 9:
		month_text = "septembre"
	elif month == 10:
		month_text = "octobre"
	elif month == 11:
		month_text = "novembre"
	elif month == 12:
		month_text = "decembre"
	day = date.day
	return render(request,'tennis/home.html',locals())

def qcq(request):
	return render(request,'tennis/404.html',locals())

def sponsors(request):
	return render(request,'tennis/sponsors.html',locals())

def allResult(request):
	info = infoTournoi.objects.all()
	return render(request,'tennis/resultatAll.html',locals())

def resultat(request,id):
	info = infoTournoi.objects.get(edition=id)
	#Resultat du tournoi des familles
	ti = TournoiTitle.objects.get(nom="Tournoi des familles")
	famille = info.resultats.filter(tournoi__titre=ti)
	if len(famille) > 0:
		famille = famille[0]

	#Resultat du Double mixte
	ti = TournoiTitle.objects.get(nom="Double mixte")
	mixte = info.resultats.filter(tournoi__titre=ti)

	#Resultat du Double femmes
	ti = TournoiTitle.objects.get(nom="Double femmes")
	femmes = info.resultats.filter(tournoi__titre=ti)

	#Resultat du Double hommes
	ti = TournoiTitle.objects.get(nom="Double hommes")
	hommes = info.resultats.filter(tournoi__titre=ti)

	ti = None

	return render(request,'tennis/resultat.html',locals())

def contact(request):
	return render(request,'tennis/contact.html',locals())

def tournoi(request):
	if request.user.is_authenticated():
		if Participant.objects.get(user=request.user).isAccountActivated:
			nonComfirme = request.user.user1.filter(confirm=False)
			demande = request.user.user2.filter(confirm=False)
			inscrit1 = request.user.user1.filter(confirm=True)
			inscrit2 = request.user.user2.filter(confirm=True)
			inscrit =  list(chain(inscrit1,inscrit2))
			agenda = False
			info = infoTournoi.objects.all()
			info = info.order_by("edition")[len(info)-1]
			date1 = info.date
			date2 = date1 + datetime.timedelta(days=1)
			for elem in inscrit:
				if elem.tournoi.titre.jour == "Samedi":
					elem.date = date1.strftime('%d/%m/%Y')
				else:
					elem.date = date2.strftime('%d/%m/%Y')
				if elem.valid and elem.tournoi.status.numero >= 2:
					agenda = True
			return render(request,'tennis/tournoi.html',locals())
		else:
			return render(request,'tennis/tournoiUserNotValidated.html',locals())
	return redirect(reverse(home))

def inscriptionTournoi(request):
	page = 1
	pageLength = 10
	recherche = ""
	if request.method == 'POST':
		if request.POST['action'] == "search":
			page = request.POST['page']
			recherche = request.POST['rechercheField'].strip()

	Ex = Extra.objects.only
	Tour = Tournoi.objects.all()
	#Liste des user ordered et sans sois meme
	Use = User.objects.all().order_by('username').exclude(username=request.user.username)
	#On retire les staff et les admins
	Use = Use.exclude(is_staff=True).exclude(groups__name="Admin").exclude(groups__name="staff")

	if recherche != "":
		Use = Use.filter(
			Q(username__icontains=recherche) |
			Q(participant__nom__icontains=recherche) | 
			Q(participant__prenom__icontains=recherche))	

	#Utilisateur courant
	u = request.user

	print(u.user_permissions.all())

	#Recuperations des infos
	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	today = info.date

	#Tri de la liste
	
	#Libre samedi/dimanche
	libre_Samedi = True
	libre_Dimanche = True
	for elem in u.user1.all() or u.user2.all():
		if elem.tournoi.titre.jour == "Samedi":
			libre_Samedi = False
		else:
			libre_Dimanche = False

	famille_25 = yearsago(25, today)
	famille_15 = yearsago(15, today)
	
	querysets = list()
	#Liste contenant les utilisateurs pour le tournoi des familles
	famille_list = list()
	if libre_Samedi:
		#Check tournoi des familles
		#- de 15 ans
		if u.participant.datenaissance >= famille_15:
			#On garde les utilisateur de + de 25 ans
			famille_list = Use.filter(participant__datenaissance__lte=famille_25)
			#On retire ceux qui ne sont pas libre le samedi
			famille_list = famille_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(user2__tournoi__titre__jour="Samedi")
			querysets.append(famille_list)
		#+ de 25 ans
		elif u.participant.datenaissance <= famille_25:
			#On garde les utilisateur de - de 15 ans
			famille_list = Use.filter(participant__datenaissance__gte=famille_15)
			#On retire ceux qui ne sont pas libre le samedi
			famille_list = famille_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(user2__tournoi__titre__jour="Samedi")
			querysets.append(famille_list)

	#Liste du samedi (except tournoi des familles)
	samedi_list = list()
	if libre_Samedi:
		#On prend seulement les joueur du sexe opposé
		samedi_list = Use.exclude(participant__titre=u.participant.titre)
		#On retire ceux qui ne sont pas libre samedi
		samedi_list = samedi_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(user2__tournoi__titre__jour="Samedi")
		querysets.append(samedi_list)

	#Liste du dimanche
	dimanche_list = list()
	if libre_Dimanche:
		#On prend seulement les joueurs du meme sexe
		dimanche_list = Use.filter(participant__titre=u.participant.titre)
		#On retire ceux qui ne sont pas libre dimanche
		dimanche_list = dimanche_list.exclude(user1__tournoi__titre__jour="Dimanche").exclude(user2__tournoi__titre__jour="Dimanche")
		querysets.append(dimanche_list)

	debut = ((int(page)-1)*pageLength)+1
	fin = debut + (pageLength-1)
	length = 0
	if len(querysets) > 0:
		#Merge query sets
		Use = reduce(or_, querysets[1:], querysets[0])
		length = len(Use)
		Use = Use[debut-1:fin]
	else:
		Use = list()

	#calcul des ages des users
	born = request.user.participant.datenaissance
	request.user.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

	for u in Use:
		born = u.participant.datenaissance
		u.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))


	if request.method == "POST":
		if request.POST['action'] == "formPair":
			#On recupère les donnée du formualaire
			username2 = request.POST['username2']
			comment1 = request.POST['remarque']
			title_tournoi = request.POST['title_tournoi']
			categorie_tournoi = request.POST['categorie_tournoi']
			if categorie_tournoi == "-":
				categorie_tournoi = title_tournoi
			#On recupere le tournoi en fonction du titre et de la categorie
			t = TournoiTitle.objects.get(nom=title_tournoi)
			c = TournoiCategorie.objects.get(nom=categorie_tournoi)
			tournois = Tournoi.objects.get(titre=t,categorie=c)
			extra = request.POST.getlist('extra')
			#On recupere les extras pris par l'utilisateur
			extra1 = list()
			for elem in extra:
				extra1.append(Extra.objects.get(id=elem))
			#On en déduit les extras non pris par l'utilisateur
			extranot1 = list()
			Ex = Extra.objects.all()
			for elem in Ex:
				contained = False
				for el in extra1:
					if elem.id == el.id:
						contained = True
				if contained == False:
					extranot1.append(Extra.objects.get(id=elem.id))

			#On vérifie que l'utilisateur a bien rentré un deuxieme joueur
			if (username2==""):
				errorAdd = "Veuillez rajouter un deuxieme joueur pour votre pair"
				return render(request,'tennis/inscriptionTournoi.html',locals())

			#On véririe qu'il ne s'est pas entré lui meme
			user1 = User.objects.get(username=request.user.username)
			user2 = User.objects.get(username=username2)

			if (user1==user2):
				errorAdd = "Vous ne pouvez pas faire une pair avec vous meme"
				return render(request,'tennis/inscriptionTournoi.html',locals())

			#Série de vérification pour que l'utilisateur ou son partenaire ne soit pas inscrit dans un tournoi du meme jour
			user1Tournoi1 = user1.user1.all()
			user1Tournoi2 = user1.user2.all()

			user2Tournoi1 = user2.user1.all()
			user2Tournoi2 = user2.user2.all()

			for elem in user1Tournoi1:
				if(elem.tournoi.titre.jour == tournois.titre.jour):
					errorAdd = "Vous etes deja inscrit a un tournoi ce jour!"
					return render(request,'tennis/inscriptionTournoi.html',locals())

			for elem in user1Tournoi2:
				if(elem.tournoi.titre.jour == tournois.titre.jour):
					errorAdd = "Vous etes deja inscrit a un tournoi ce jour!"
					return render(request,'tennis/inscriptionTournoi.html',locals())

			for elem in user2Tournoi1:
				if(elem.tournoi.titre.jour == tournois.titre.jour and elem.confirm):
					errorAdd = "Le joueur 2 est deja inscrit dans un tournoi ce jour!"
					return render(request,'tennis/inscriptionTournoi.html',locals())

			for elem in user2Tournoi2:
				if(elem.tournoi.titre.jour == tournois.titre.jour and elem.confirm):
					errorAdd = "Le joueur 2 est deja inscrit dans un tournoi ce jour!"
					return render(request,'tennis/inscriptionTournoi.html',locals())

			#On cré la pair
			pair = Pair(tournoi = tournois,user1=user1,user2=user2,comment1 = comment1,confirm = False,valid = False,pay = False)
			pair.save()
			#On rajoute les extras
			for elem in extra:
				ext = Extra.objects.get(id=elem)
				pair.extra1.add(ext)

			# Send mail
			send_confirmation_email_pair_registered(Participant.objects.get(user=pair.user1), Participant.objects.get(user=pair.user2))

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
	pair = Pair.objects.get(id=id)
	if pair.user2 != request.user:
		return redirect(reverse(tournoi))
	if request.method == "POST":
		if request.POST['action'] == "validate":
			remarque = request.POST['remarque']
			extra = request.POST.getlist('extra')



			pair.confirm = True
			pair.comment2 = remarque
			pair.save()

			for elem in extra:
				ext = Extra.objects.get(id=elem)
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
				extranot1.append(Extra.objects.get(id=elem.id))




		return render(request,'tennis/confirmPair.html',locals())
	return redirect(reverse(home))

def cancelPair(request,id):
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.get(id=id)
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
				extranot1.append(Extra.objects.get(id=elem.id))

		return render(request,'tennis/cancelPair.html',locals())
	return redirect(reverse(home))

def viewPair(request,id):
	if request.method == "POST":
		pair = Pair.objects.filter(id=id)
		pair.delete()
		return redirect(reverse(tournoi))
	pair = Pair.objects.filter(id=id)
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.get(id=id)
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
				extranot1.append(Extra.objects.get(id=elem.id))

		extra2 = pair.extra2.all()
		extranot2 = list()
		for elem in Ex:
			contained = False
			for el in extra2:
				if elem.id == el.id:
					contained = True
			if contained == False:
				extranot2.append(Extra.objects.get(id=elem.id))
		return render(request,'tennis/viewPair.html',locals())
	return redirect(reverse(home))

def payPair(request,id):
	pair = Pair.objects.filter(id=id)
	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	prix = info.prix
	if len(pair) <1:
		return redirect(reverse(tournoi))
	pair = Pair.objects.get(id=id)
	if pair.user1 != request.user and pair.user2 != request.user:
		return redirect(reverse(tournoi))
	if request.user.is_authenticated():
		#TODO check si il peut payer cette pair
		allExtras = Extra.objects.all()
		extra1 = pair.extra1.all()
		extra2 = pair.extra2.all()
		totalprice = 2*prix
		listUniqueExtra = list(set(list(extra1) + list(extra2)))
		extraList = []
		for extra in listUniqueExtra:
			count = 0
			for e1 in extra1:
				if extra.id == e1.id:
					count += 1
			for e2 in extra2:
				if extra.id == e2.id:
					count += 1
			extraList.append((extra.nom, extra.prix, count))
			totalprice += float(count*extra.prix)

		return render(request,'tennis/payPair.html',locals())
	return redirect(reverse(home))

def enterScore(request,id):
	def is_number(s):
		try:
			float(s)
			return True
		except ValueError:
			return False
	poule = Poule.objects.get(id=id)
	if request.method == "POST":
		poule.score.all().delete()
		pairList = poule.paires.all()
		dictionnaire = dict()
		for id1 in pairList:
			for id2 in pairList:
				if((str(id1.id)+"-"+str(id2.id) in dictionnaire) or (str(id2.id)+"-"+str(id1.id) in dictionnaire) or (id1==id2)):
					pass
				else:
					dictionnaire[str(id1.id)+"-"+str(id2.id)] = True
					dictionnaire[str(id2.id)+"-"+str(id1.id)] = True

					if (is_number(request.POST[str(id1.id)+"-"+str(id2.id)]) and is_number(request.POST[str(id2.id)+"-"+str(id1.id)])):
						score = Score(paire1 = id1,paire2=id2,point1=int(request.POST[str(id1.id)+"-"+str(id2.id)]),point2=int(request.POST[str(id2.id)+"-"+str(id1.id)]))
						score.save()
						poule.score.add(score)

		return redirect(reverse(tournoi))

	if request.user.is_authenticated():
		scoreList = poule.score.all()
		scoreValues = ""
		for sco in scoreList:
			scoreValues = scoreValues + repr(sco.paire1.id)+"-"+repr(sco.paire2.id)+","+repr(sco.point1)+"."+repr(sco.paire2.id)+"-"+repr(sco.paire1.id)+","+repr(sco.point2)+"."
		scoreValues = scoreValues[:-1]
		return render(request,'tennis/playerScore.html',locals())
	return redirect(reverse(home))


def terrain(request):
	if request.user.is_authenticated():
		if Participant.objects.get(user=request.user).isAccountActivated:
			court = Court.objects.filter(user=request.user)
			return render(request,'tennis/terrain.html',locals())
		else:
			return render(request,'tennis/terrainUserNotValidated.html',locals())
	return redirect(reverse(home))

def registerTerrain(request):
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	if request.method == "POST":
		rue = request.POST['street']
		numero = request.POST['number']
		boite = request.POST['boite']
		postalcode = request.POST['postalcode']
		locality = request.POST['locality']
		lat = request.POST['lat']
		lng = request.POST['lng']
		acces = request.POST['acces']
		matiere = (u'' + request.POST['matiere']).encode('utf-8')
		type = (u'' + request.POST['type']).encode('utf-8')
		etat = (u'' + request.POST['etat']).encode('utf-8')
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
		court = Court(rue = rue,numero=numero,boite=boite,codepostal=postalcode,localite=locality,acces=acces,matiere=CourtSurface.objects.get(nom=matiere),type=CourtType.objects.get(nom=type),dispoDimanche=dispoDimanche,dispoSamedi=dispoSamedi,etat=CourtState.objects.get(nom=etat),commentaire=commentaire,user = request.user,latitude=lat,longitude=lng)

		# Send confirmation mail
		send_confirmation_email_court_registered(Participant.objects.get(user=request.user), court)

		court.save()

		return redirect(reverse(terrain))

	if request.user.is_authenticated():
		return render(request,'tennis/registerTerrain.html',locals())
	return redirect(reverse(home))

def editTerrain(request,id):
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	court = Court.objects.filter(id=id)

	if len(court) <1:
		return redirect(reverse(terrain))
	court = Court.objects.get(id=id)
	if court.user != request.user:
		return redirect(reverse(terrain))

	if request.method == "POST":
		if request.POST['action'] == "modifyCourt":
			rue = request.POST['street']
			numero = request.POST['number']
			boite = request.POST['boite']
			postalcode = request.POST['postalcode']
			locality = request.POST['locality']
			lat = request.POST['lat']
			lng = request.POST['lng']
			acces = request.POST['acces']
			matiere = (u'' +request.POST['matiere']).encode('utf-8')
			type = (u'' + request.POST['type']).encode('utf-8')
			etat = (u'' + request.POST['etat']).encode('utf-8')
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
			court.matiere=CourtSurface.objects.get(nom=matiere)
			court.type=CourtType.objects.get(nom=type)
			court.dispoDimanche=dispoDimanche
			court.dispoSamedi=dispoSamedi
			court.etat=CourtState.objects.get(nom=etat)
			court.commentaire=commentaire
			court.user = request.user
			court.latitude = lat
			court.longitude = lng
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

'''
def staff(request):
	if request.user.is_authenticated():
		return render(request,'tennis/staff.html',locals())
	return redirect(reverse(home))
'''

#TODO permission QUENTIN GUSBIN
def staffTournoi(request):
	if request.user.is_authenticated():
		allTitre = TournoiTitle.objects.all()
		allTournoi = Tournoi.objects.all()
		for tourn in allTournoi:
			nbrPair = len(Pair.objects.filter(tournoi=tourn,valid=True))
			tourn.np = nbrPair
			pouleLength = len(Poule.objects.filter(tournoi=tourn))
			tourn.pl = pouleLength
		return render(request,'tennis/staffTournoi.html',locals())
	return redirect(reverse(home))

def pouleTournoi(request,name):
	def getKey(item):
		return item[1]

	if request.method == "POST":
		title = name
		cat = name
		if "_" in name:
			title = name.split("_")[0]
			cat = name.split("_")[1]
		ti = TournoiTitle.objects.get(nom=title)
		ca = TournoiCategorie.objects.get(nom=cat)
		tournoi = Tournoi.objects.get(titre=ti,categorie=ca)
		s = TournoiStatus.objects.get(numero=1)
		tournoi.status = s
		a = tournoi.arbre
		tournoi.arbre = None
		tournoi.save()
		LogActivity(user=request.user,section="Poules",details="Suppressions des poules du tournoi : "+tournoi.nom()).save()
		return redirect(reverse(generatePool,args={name}))

	if request.user.is_authenticated():
		title = name
		cat = name
		if "_" in name:
			title = name.split("_")[0]
			cat = name.split("_")[1]
		ti = TournoiTitle.objects.get(nom=title)
		ca = TournoiCategorie.objects.get(nom=cat)
		tournoi = Tournoi.objects.get(titre=ti,categorie=ca)
		poules = Poule.objects.filter(tournoi=tournoi)
		dictionnaire = dict()
		x = 0
		for poule in poules:
			if x % 2 == 0 :
				poule.newRow = True
			else:
				poule.newRow = False
			x += 1
			if poule.status == PouleStatus.objects.get(numero=2):
				scores = poule.score.all()
				dico = dict()
				for paire in poule.paires.all():
					dico[paire.id] = 0
				for score in scores:
					dico[score.paire1.id] = dico[score.paire1.id]+score.point1
					dico[score.paire2.id] = dico[score.paire2.id]+score.point2
				liste = list()
				for key,value in dico.items():
					liste.append((key,value))
				liste = sorted(liste,key=getKey,reverse=True)
				dictionnaire[poule.id] = liste
				poule.SortedPair = list()
				for pairID, sc in liste:
					pai = Pair.objects.get(id=pairID)
					pai.score = sc
					poule.SortedPair.append(pai)

		return render(request,'tennis/pouleTournoi.html',locals())
	return redirect(reverse(home))

#TODO permissions QUENTIN GUSBIN
def knockOff(request,name):
	title = name
	cat = name
	if "_" in name:
		title = name.split("_")[0]
		cat = name.split("_")[1]
	ti = TournoiTitle.objects.get(nom=title)
	ca = TournoiCategorie.objects.get(nom=cat)
	tournoi = Tournoi.objects.get(titre=ti,categorie=ca)
	#Liste des tournoi qui ont deja un arbre
	all_tournoi_with_arbre = Tournoi.objects.filter(arbre__id__gte=0).exclude(titre=ti,categorie=ca)
	court_list = dict()

	for elem in all_tournoi_with_arbre:
		if elem.arbre.court.id in court_list:
			court_list[elem.arbre.court.id] += "<br>" + str(elem)
		else:
			court_list[elem.arbre.court.id] = str(elem)


	all_tournoi_with_arbre = None

	terrains = Court.objects.filter(valide=True)

	jour = ti.jour
	if(jour =="Samedi"):
		terrains = terrains.filter(dispoSamedi=True)
	else:
		terrains = terrains.filter(dispoDimanche=True)

	terrains.order_by("id")

	

	for elem in terrains:
		if elem.id in court_list: 
			elem.conflict = court_list[elem.id]
		else:
			elem.conflict = ""

	court_list = None
	def getKey(item):
		return item[1]
	if request.method == "POST":
		if request.POST['action'] == "save":
			treeData = request.POST['treeData']
			treeLabel = request.POST['treeLabel']
			gagnant = request.POST['gagnant']
			finaliste = request.POST['finaliste']
			terrainRecv = request.POST['terrain']
			terrain = Court.objects.get(id=terrainRecv)
			print(terrain)
			pair_g = None
			if(gagnant != ""):
				pairgagnante = Pair.objects.get(id=int(gagnant))
				pairgagnante.gagnant = True
				pairgagnante.save()
				pair_g = pairgagnante

			pair_f = None
			if(finaliste != ""):
				finalistes = finaliste.split("-")
				finaliste1 = Pair.objects.get(id=int(finalistes[0]))
				finaliste2 = Pair.objects.get(id=int(finalistes[1]))
				finaliste1.finaliste = True
				finaliste1.save()
				finaliste2.finaliste = True
				finaliste2.save()
				if pair_g is not None:
					if pair_g == finaliste1:
						pair_f = finaliste2
					else:
						pair_f = finaliste1

			if pair_g is not None and pair_f is not None:
				#Changement du status du tournoi
				s = TournoiStatus.objects.get(numero=4)
				tournoi.status = s
				tournoi.save()

				#Save des resultats
				for elem in Resultat.objects.filter(tournoi=tournoi):
					elem.delete()
				ga = str(pair_g.user1.participant.prenom) +" "+ str(pair_g.user1.participant.nom).upper() +" et "+str(pair_g.user2.participant.prenom) +" "+ str(pair_g.user2.participant.nom).upper()
				fi = str(pair_f.user1.participant.prenom) +" "+ str(pair_f.user1.participant.nom).upper() +" et "+str(pair_f.user2.participant.prenom) +" "+ str(pair_f.user2.participant.nom).upper()
				r = Resultat(tournoi=tournoi,gagnants_alt=ga,finalistes_alt=fi)
				r.save()
				r.gagnants.add(pair_g.user1)
				r.gagnants.add(pair_g.user2)
				r.finalistes.add(pair_f.user1)
				r.finalistes.add(pair_f.user2)
				r.save()
				info = infoTournoi.objects.all()
				info = info.order_by("edition")[len(info)-1]
				info.resultats.add(r)
				info.save()

			if tournoi.arbre is None:
				arbre = Arbre(data = treeData,label = treeLabel)
				arbre.court = terrain
				arbre.save()
				tournoi.arbre = arbre
				tournoi.save()
			else:
				arbre = tournoi.arbre
				arbre.data = treeData
				arbre.label= treeLabel
				arbre.court = terrain
				arbre.save()
				LogActivity(user=request.user,section="Tournoi",details="Mise a jour de l'abre du tournoi : "+tournoi.nom()).save()

		elif request.POST['action'] == "deleteTree":
			s = TournoiStatus.objects.get(numero=3)
			tournoi.status = s
			tournoi.save()
			if tournoi.arbre is not None:
				for poule in tournoi.poule_set.all():
					for pair in poule.paires.all():
						pair.gagnant = False
						pair.finaliste = False
						pair.save()
				arbre = tournoi.arbre
				arbre.data = None
				arbre.label = None
				arbre.save()
				LogActivity(user=request.user,section="Tournoi",details="Suppression de l'abre du tournoi : "+tournoi.nom()).save()
				return redirect(reverse(knockOff,args={name}))

	if request.user.is_authenticated():

		poules = Poule.objects.filter(tournoi=tournoi)
		dictionnaire = dict()
		allPaires = list()
		for poule in poules:
			if poule.status == PouleStatus.objects.get(numero=2):
				scores = poule.score.all()
				dico = dict()
				for paire in poule.paires.all():
					dico[paire.id] = 0
				for score in scores:
					dico[score.paire1.id] = dico[score.paire1.id]+score.point1
					dico[score.paire2.id] = dico[score.paire2.id]+score.point2
				liste = list()
				for key,value in dico.items():
					liste.append((key,value))
				liste = sorted(liste,key=getKey,reverse=True)
				dictionnaire[poule.id] = liste
				poule.SortedPair = list()
				x = 1
				for pairID, sc in liste:
					pai = Pair.objects.get(id=pairID)
					pai.score = sc
					pai.poule = poule.id
					pai.position = x
					poule.SortedPair.append(pai)
					allPaires.append(pai)
					x = x +1
		if tournoi.arbre is not None:
			arbre = tournoi.arbre
		return render(request,'tennis/knockOff.html',locals())
	return redirect(reverse(home))

#TODO permission QUENTIN GUSBIN
def pouleScore(request,id):
	def is_number(s):
		try:
			float(s)
			return True
		except ValueError:
			return False
	poule = Poule.objects.get(id=id)
	if request.method == "POST":
		if request.POST['action'] == 'save':
			poule.status = PouleStatus.objects.get(numero=1)
			poule.save()
		elif request.POST['action'] == 'saveFinite':
			poule.status = PouleStatus.objects.get(numero=2)
			poule.save()
			#Check si toutes les poules sont finite
			valid = True
			for elem in Poule.objects.filter(tournoi=poule.tournoi):
				if elem.status.numero != 2:
					valid = False
					break
			if valid :
				t = poule.tournoi
				t.status = TournoiStatus.objects.get(numero=3)
				t.save()
			LogActivity(user=request.user,section="Tournoi",details="Mise a jour des point de la poule "+id+" dans le tournoi ").save()
		poule.score.all().delete()
		pairList = poule.paires.all()
		dictionnaire = dict()
		for id1 in pairList:
			for id2 in pairList:
				if((str(id1.id)+"-"+str(id2.id) in dictionnaire) or (str(id2.id)+"-"+str(id1.id) in dictionnaire) or (id1==id2)):
					pass
				else:
					dictionnaire[str(id1.id)+"-"+str(id2.id)] = True
					dictionnaire[str(id2.id)+"-"+str(id1.id)] = True

					if (is_number(request.POST[str(id1.id)+"-"+str(id2.id)]) and is_number(request.POST[str(id2.id)+"-"+str(id1.id)])):
						score = Score(paire1 = id1,paire2=id2,point1=int(request.POST[str(id1.id)+"-"+str(id2.id)]),point2=int(request.POST[str(id2.id)+"-"+str(id1.id)]))
						score.save()
						poule.score.add(score)

		if request.POST['action'] == 'save':
			return redirect(reverse(pouleScore,args={id}))
		elif request.POST['action'] == 'saveFinite':
			return redirect(reverse(pouleTournoi,args={poule.tournoi.nom()}))

		return redirect(reverse(staffTournoi))
	if request.user.is_authenticated():
		scoreList = poule.score.all()
		scoreValues = ""
		for sco in scoreList:
			scoreValues = scoreValues + repr(sco.paire1.id)+"-"+repr(sco.paire2.id)+","+repr(sco.point1)+"."+repr(sco.paire2.id)+"-"+repr(sco.paire1.id)+","+repr(sco.point2)+"."
		scoreValues = scoreValues[:-1]
		return render(request,'tennis/pouleScore.html',locals())
	return redirect(reverse(home))

#TODO permission QUENTIN GUSBIN
def generatePool(request,name):
	title = name
	cat = name
	if "_" in name:
		title = name.split("_")[0]
		cat = name.split("_")[1]
	ti = TournoiTitle.objects.get(nom=title)
	ca = TournoiCategorie.objects.get(nom=cat)
	tournoi = Tournoi.objects.get(titre=ti,categorie=ca)
	terrains = Court.objects.filter(valide=True)
	allPair = Pair.objects.filter(tournoi=tournoi, valid=True)
	poules = Poule.objects.filter(tournoi=tournoi)

	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	infTournoi = info
	infLng = infTournoi.longitude
	infLat = infTournoi.latitude
	
	jour = tournoi.titre.jour
	if(jour =="Samedi"):
		terrains = terrains.filter(dispoSamedi=True)
	else:
		terrains = terrains.filter(dispoDimanche=True)

	terrains.order_by('id')

	if request.method == "POST":


		terrainsList = request.POST['assignTerrains'].split('-')
		terrainsList.pop()

		leadersList = request.POST['assignLeaders'].split('/')
		leadersList.pop()

		pairspoulesList = request.POST['assignPairPoules'].split('-')
		pairspoulesList.pop()


		if request.POST['action'] == 'save':
			tournoi.status = TournoiStatus.objects.get(numero=1)
			tournoi.save()
		elif request.POST['action'] == 'saveFinite':
			tournoi.status = TournoiStatus.objects.get(numero=2)
			tournoi.save()
			LogActivity(user=request.user,section="Tournoi",details="Generation des poules du tournoi : "+tournoi.nom()).save()


		i = 0
		j = -1
		pouleDict = {}
		while (i < len(pairspoulesList)):
			if pairspoulesList[i].startswith('[') and pairspoulesList[i].endswith(']'):
				j += 1
				pouleDict[j] = {}
				pouleDict[j]['pairList'] = []
				if terrainsList[j] != '':
					pouleDict[j]['terrain'] = Court.objects.get(id=terrainsList[j])
				pouleDict[j]['leaderName'] = leadersList[j]
			else:
				pair = Pair.objects.get(id=pairspoulesList[i])
				pouleDict[j]['pairList'].append(pair)
				user1fullname = pair.user1.participant.prenom + ' ' +pair.user1.participant.nom
				user2fullname = pair.user2.participant.prenom + ' ' +pair.user2.participant.nom
				if user1fullname == pouleDict[j]['leaderName']:
					pouleDict[j]['leader'] = pair.user1
				elif user2fullname == pouleDict[j]['leaderName']:
					pouleDict[j]['leader'] = pair.user2

			i += 1
		i = 0

		#Au lieu de delete on parcours la liste
		#Poule.objects.filter(tournoi=tournoi).delete()
		score_list = list()
		#On parcours et on garde les scores
		for elem in Poule.objects.filter(tournoi=tournoi):
			p2 = Poule(tournoi=tournoi)
			p2.status = elem.status
			p2.save()
			for p in elem.paires.all():
				p2.paires.add(p)
			for p in elem.score.all():
				p2.score.add(p)
			score_list.append(p2)
			elem.delete()

		finali = True
		while (i <= j):
			p = Poule(tournoi=tournoi)
			p.status = PouleStatus.objects.get(numero=0)
			p.save()
			if 'leader' in pouleDict[i]:
				p.leader = pouleDict[i]['leader']
			if 'terrain' in pouleDict[i]:
				p.court = pouleDict[i]['terrain']
			for pair in pouleDict[i]['pairList']:
				p.paires.add(pair)

			p.save()
			#check si c'est les meme pair qu'une des liste
			for elem in score_list:
				pair_list = sorted(elem.paires.all(),key=lambda x: x.id)
				pair_list2 = sorted(p.paires.all(),key=lambda x: x.id)
				if pair_list == pair_list2:
					p.score = elem.score.all()
					p.status = elem.status
					if p.status.numero < 2:
						finali = False
					break
				else:
					finali = False
			i += 1
			p.save()

		for elem in score_list:
			elem.delete()

		if finali :
			tournoi.status = TournoiStatus.objects.get(numero=3)
			tournoi.save()
		else:
			tournoi.status = TournoiStatus.objects.get(numero=2)
			tournoi.save()


		if request.POST['action'] == 'save':
			tournoi.status = TournoiStatus.objects.get(numero=1)
			tournoi.save()
			return redirect(reverse(generatePool,args={tournoi.nom()}))
			#request.method = "GET"
			#return generatePool(request,tournoi.nom)
			#return HttpResponseRedirect('/tennis/staff/tournois/%s'%tournoi.nom)
		else:
			return redirect(reverse(staffTournoi))
	if request.user.is_authenticated():
		

		listTerrains = list(terrains)
		listTerrainSaved = list()
		listLeaderSaved = list()
		nbrTerrains = len(listTerrains)

		# TODO Restaurer la sauvergarde
		listPoules = list(poules)

		if len(listPoules) == 0:
			saved = False

			defaultSize = 6.0
			defaultValue = int(math.ceil((len(allPair)/defaultSize)))
			poolRange = range(0,defaultValue)
			pairListAll = dict()
			for x in range(0,defaultValue):
				index = int(x*defaultSize)
				pairListAll[x+1] = (allPair[index:index+int(defaultSize)])
				if x==defaultValue-1 :
					v = int(defaultSize) - len(pairListAll[x+1])
			today = date.today()
			for elem in allPair:
				u1 = elem.user1
				born = u1.participant.datenaissance
				u1.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
				u2 = elem.user2
				born = u2.participant.datenaissance
				u2.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
				c1 = ""
				c2 = ""
				if elem.comment1:
					c1 = str(elem.comment1)
				if elem.comment2:
					c2 = str(elem.comment2)
				if c1 != "" or c2 != "":
					elem.commentaires = c1 + "<hr>" + c2
			return render(request,'tennis/generatePool.html',locals())
		else:
			saved = True

			defaultValue = len(listPoules)
			defaultSize = 0
			pairListAll = dict()
			today = date.today()
			i = 0
			for poule in listPoules:
				pairListAll[i+1] = []
				listTerrainSaved.append(poule.court)
				listLeaderSaved.append(poule.leader)
				if defaultSize < len(poule.paires.all()):
					defaultSize = len(poule.paires.all())
				for elem in poule.paires.all():
					u1 = elem.user1
					born = u1.participant.datenaissance
					u1.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
					u2 = elem.user2
					born = u2.participant.datenaissance
					u2.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
					c1 = ""
					c2 = ""
					if elem.comment1:
						c1 = str(elem.comment1)
					if elem.comment2:
						c2 = str(elem.comment2)
					if c1 != "" or c2 != "":
						elem.commentaires = c1 + "<hr>" + c2
					pairListAll[i+1].append(elem)
				i += 1
			poolRange = range(0, defaultValue)
			return render(request,'tennis/generatePool.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def staffTerrain(request):
	page = 1
	pageLength = 10
	recherche = ""
	material = ""
	validation = ""
	used = ""
	dispo = ""
	state = ""
	typeCourt = ""
	veteran = ""
	if request.method == 'POST':
		page = request.POST['page']
		pageLength = int(request.POST['pagelength'])
		recherche = request.POST['rechercheField'].strip()
		material = request.POST['material']
		validation = request.POST['validation']
		used = request.POST['used']
		dispo = request.POST['dispo']
		state = request.POST['state']
		typeCourt = request.POST['type']
		veteran = request.POST['veteran']

	allCourt = Court.objects.all()

	#Recherche
	if recherche != "":
		allCourt = allCourt.filter(
			Q(id__icontains=recherche) |
			Q(user__username__icontains=recherche) | 
			Q(user__participant__nom__icontains=recherche) | 
			Q(user__participant__prenom__icontains=recherche) |
			Q(numero__icontains=recherche) | 
			Q(rue__icontains=recherche) | 
			Q(localite__icontains=recherche) | 
			Q(codepostal__icontains=recherche))	

	if material != "":
		allCourt = allCourt.filter(matiere=material)

	if validation != "":
		if validation == "True":
			allCourt = allCourt.filter(valide=True)
		else:
			allCourt = allCourt.filter(valide=False)

	if used != "":
		if used == "True":
			allCourt = allCourt.filter(poule__id__gte=0).distinct()
		else:
			allCourt = allCourt.exclude(poule__id__gte=0)

	if dispo != "":
		#samedi
		if dispo == "1":
			allCourt = allCourt.filter(dispoSamedi=True)
		#dimanche
		elif dispo == "2":
			allCourt = allCourt.filter(dispoDimanche=True)
		#samedi et dimanche
		else:
			allCourt = allCourt.filter(dispoSamedi=True,dispoDimanche=True)

	if state != "":
		allCourt = allCourt.filter(etat=state)

	if typeCourt != "":
		allCourt = allCourt.filter(type=typeCourt)

	if veteran != "":
		if veteran == "True":
			allCourt = allCourt.filter(usedLastYear=True)
		else:
			allCourt = allCourt.filter(usedLastYear=False)


	allCourt = allCourt.order_by("id")

	length = len(allCourt)
	debut = ((int(page)-1)*pageLength)+1
	fin = debut + (pageLength-1)
	allCourt = allCourt[debut-1:fin]

	for court in allCourt:
		if len(court.poule_set.all()) > 0:
			court.used = True
		else:
			court.used = False
	
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	if request.user.is_authenticated():
		return render(request,'tennis/staffTerrain.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def staffPaire(request):
	page = 1
	pageLength = 10
	recherche = ""
	validation = ""
	paiement = ""
	tournoi = ""
	if request.method == 'POST':
		page = request.POST['page']
		pageLength = int(request.POST['pagelength'])
		recherche = request.POST['rechercheField'].strip()
		validation = request.POST['validation']
		paiement = request.POST['paiement']
		tournoi = request.POST['tournoi']

	allPair = Pair.objects.all()

	if recherche != "":
		allPair = allPair.filter(
			Q(id__icontains=recherche) |
			Q(user1__username__icontains=recherche) | 
			Q(user1__participant__nom__icontains=recherche) | 
			Q(user1__participant__prenom__icontains=recherche) |
			Q(user2__username__icontains=recherche) | 
			Q(user2__participant__nom__icontains=recherche) | 
			Q(user2__participant__prenom__icontains=recherche))	

	if validation != "":
		if validation == "True":
			allPair = allPair.filter(valid = True)
		else:
			allPair = allPair.filter(valid = False)

	if paiement != "":
		if paiement == "True":
			allPair = allPair.filter(pay = True)
		else:
			allPair = allPair.filter(pay = False)

	if tournoi != "":
		title = tournoi
		cat = tournoi
		if "_" in tournoi:
			title = tournoi.split("_")[0]
			cat = tournoi.split("_")[1]
		t = TournoiTitle.objects.get(nom=title)
		c = TournoiCategorie.objects.get(nom=cat)
		new_tournoi = Tournoi.objects.get(titre=t,categorie=c)
		allPair = allPair.filter(tournoi=new_tournoi)

	allPair = allPair.order_by("id")
	length = len(allPair)
	debut = ((int(page)-1)*pageLength)+1
	fin = debut + (pageLength-1)
	allPair = allPair[debut-1:fin]
	Tour = Tournoi.objects.all()

	if request.user.is_authenticated():
		return render(request,'tennis/staffPair.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Extra')
def staffExtra(request):
	def is_number(s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	extras = Extra.objects.all()
	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	prix_inscription = info.prix
	date_inscription = info.date
	formated_date = date_inscription.strftime('%d/%m/%Y')
	yearLoop = range(date.today().year,date.today().year+5)
	isAdmin = request.user.groups.filter(name="Admin").exists()

	if request.method == "POST":
		if request.POST['action'] == "cleanDb":
			resetDbForNextYear(request)

		if request.POST['action'] == "modifyInfoTournoi":
			prixTournoi = request.POST['prixInscription'].strip()
			dateInfoTournoi = request.POST['birthdate'].strip()

			info = infoTournoi.objects.all()
			info = info.order_by("edition")[len(info)-1]
			prixTournoi = prixTournoi.replace(",",".")
			if(float(prixTournoi)>=0.0):
				info.prix = prixTournoi
				LogActivity(user=request.user,section="InfoTournoi",details=u"Prix du tournoi modifié").save()
			else:
				errorInfoPrix = "Le prix doit etre plus grand ou égale a zéro"


			splitedDateInfoTournoi = dateInfoTournoi.split("/")
			datetoEnreg = datetime.datetime(int(splitedDateInfoTournoi[2]),int(splitedDateInfoTournoi[1]),int(splitedDateInfoTournoi[0]))
			now = datetime.datetime.now()
			if(now<datetoEnreg):
				info.date = datetoEnreg
				LogActivity(user=request.user,section="InfoTournoi",details=u"Date du tournoi modifiée").save()
			else:
				errorInfoDate = "La date doit etre plus tard que maintenant"

			info.save()
			info = infoTournoi.objects.all()
			info = info.order_by("edition")[len(info)-1]
			prix_inscription = info.prix
			date_inscription = info.date
			formated_date = date_inscription.strftime('%d/%m/%Y')
			return render(request,'tennis/staffExtra.html',locals())


		if request.POST['action'] == "addExtra":
			nom = request.POST['name'].strip()
			prix = request.POST['price'].strip()
			message = request.POST['message'].strip()

			if nom=="":
				errorAdd = "Veuillez rajouter un nom à l'extra!"
				return render(request,'tennis/staffExtra.html',locals())

			if not is_number(prix):
				prix = prix.replace(",",".")
				if not is_number(prix):
					errorAdd = "Le prix n'a pas le bon format"
					return render(request,'tennis/staffExtra.html',locals())

			extra = Extra(nom=nom,prix=prix,commentaires = message)
			extra.save()
			LogActivity(user=request.user,section="Extra",details=u"Extra "+nom+ u" ajouté").save()

			successAdd = u"Extra " +nom+ u" bien ajouté!"

		if request.POST['action'] == "modifyExtra":
			id = request.POST['id']
			nom = request.POST['name']
			prix = request.POST['price']
			message = request.POST['message']

			extra = Extra.objects.get(id=id)

			if nom=="":
				errorEdit = u"Veuillez rajouter un nom à l'extra!"
				return render(request,'tennis/staffExtra.html',locals())

			if not is_number(prix) :
				prix = prix.replace(",",".")
				if not is_number(prix):
					errorEdit = u"Le prix n'a pas le bon format"
					return render(request,'tennis/staffExtra.html',locals())

			extra.nom = nom
			extra.prix = prix
			extra.commentaires = message
			extra.save()
			LogActivity(user=request.user,section="Extra",details=u"Extra " +nom+ u" modifié").save()
			successEdit = u"Extra " +nom+ u" bien modifié !"

		if request.POST['action'] == "deleteExtra":
			id = request.POST['id']
			extra = Extra.objects.get(id=id)
			extra.delete()
			LogActivity(user=request.user,section="Extra",details=u"Extra "+extra.nom+ u" delete").save()
			successDelete = u"Extra bien supprimé!"

	extras = Extra.objects.all()

	for e in extras:
		a = len(Extra.objects.filter(id=e.id,extra1__valid=True)) + len(Extra.objects.filter(id=e.id,extra2__valid=True))
		e.count = a

	if request.user.is_authenticated():
		return render(request,'tennis/staffExtra.html',locals())
	return redirect(reverse(home))


def staffLog(request):
	logs = LogActivity.objects.order_by('-date')
	if request.user.is_authenticated():
		return render(request,'tennis/staffLog.html',locals())
	return redirect(reverse(home))


@permission_required('tennis.Droit')
#TODO permission droit
def staffPerm(request):
	page = 1
	pageLength = 10
	recherche = ""
	if request.method == "POST":
		if request.POST['action'] == "search":
			page = request.POST['page']
			recherche = request.POST['rechercheField'].strip()
		else:
			usernamefield = request.POST['username']
			utilisateur = User.objects.get(username=usernamefield)
			staff = False
			if request.POST.__contains__("Tournoi des familles"):
				perm = Permission.objects.get(codename="TournoiDesFamilles")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="TournoiDesFamilles")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("Double mixte"):
				perm = Permission.objects.get(codename="DoubleMixte")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="DoubleMixte")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("Double hommes"):
				perm = Permission.objects.get(codename="DoubleHommes")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="DoubleHommes")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("Double femmes"):
				perm = Permission.objects.get(codename="DoubleFemmes")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="DoubleFemmes")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("court"):
				perm = Permission.objects.get(codename="Court")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="Court")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("pair"):
				perm = Permission.objects.get(codename="Pair")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="Pair")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("extra"):
				perm = Permission.objects.get(codename="Extra")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="Extra")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("user"):
				perm = Permission.objects.get(codename="User")
				utilisateur.user_permissions.add(perm)
				staff = True
			else:
				perm = Permission.objects.get(codename="User")
				utilisateur.user_permissions.remove(perm)

			if request.POST.__contains__("perm"):
				group = Group.objects.get(name="Admin")
				utilisateur.groups.add(group)
			else:
				group = Group.objects.get(name="Admin")
				utilisateur.groups.remove(group)

			if staff : 
				group = Group.objects.get(name="staff")
				utilisateur.groups.add(group)
			else:
				group = Group.objects.get(name="staff")
				utilisateur.groups.remove(group)

			LogActivity(user=request.user,section="Permissions",details="Changed permission of user "+utilisateur.username).save()


	Use = User.objects.all().order_by('username')

	if recherche != "":
		Use = Use.filter(
			Q(username__icontains=recherche) |
			Q(participant__nom__icontains=recherche) | 
			Q(participant__prenom__icontains=recherche))	

	Use = Use.order_by("username")
	length = len(Use)
	debut = ((int(page)-1)*pageLength)+1
	fin = debut + (pageLength-1)
	Use = Use[debut-1:fin]
	tournoiAll = TournoiTitle.objects.all()

	for u in Use:
		bd = u.participant.datenaissance
		fb = bd.strftime('%d/%m/%Y')
		u.fb = fb
	if request.user.is_authenticated():
		return render(request,'tennis/staffPerm.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.User')
def staffUser(request):
	page = 1
	pageLength = 10
	recherche = ""
	sexe = ""
	age_min = 0
	age_max = 100
	in_paire = ""
	veteran = ""
	if request.method == 'POST':
		page = request.POST['page']
		pageLength = int(request.POST['pagelength'])
		recherche = request.POST['rechercheField'].strip()
		sexe = request.POST['sex_selector']
		in_paire = request.POST['inpair']
		veteran = request.POST['veteran']
		age_min = int(request.POST['agemin'])
		age_max = int(request.POST['agemax'])

	Use = User.objects.all().order_by('username')

	#recherche sexe
	if(sexe != ""):
		Use = Use.filter(participant__titre=sexe)
	#recherche veteran
	if(veteran != ""):
		if(veteran == "True"):
			Use = Use.filter(participant__oldparticipant=True)
		else:
			Use = Use.filter(participant__oldparticipant=False)

	date_min =  yearsago(age_min)
	date_max = yearsago(age_max)

	#Recherche age min
	Use = Use.filter(participant__datenaissance__lte = date_min)

	#Recherceh age max
	Use = Use.filter(participant__datenaissance__gte = date_max)

	#recherche in paire
	if(in_paire != ""):
		if in_paire == "True":
			Use = Use.filter(Q(user1__confirm=True) | Q(user2__confirm=True))
		else:
			Use = Use.filter( ~(Q(user1__confirm=True) | Q(user2__confirm=True)))

	#recherche firld
	if(recherche != ""):
		Use = Use.filter(Q(username__icontains=recherche) | Q(participant__nom__icontains=recherche) | Q(participant__prenom__icontains=recherche))

	Use = Use.order_by("username")
	length = len(Use)
	debut = ((int(page)-1)*pageLength)+1
	fin = debut + (pageLength-1)
	Use = Use[debut-1:fin]
	

	ageRange = range(0,100)

	today = date.today()
	for u in Use:
		born = u.participant.datenaissance
		u.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
		u1_list = u.user1.all()
		u2_list = u.user2.all()
		inPair = False
		for p in u1_list or u2_list:
			if p.confirm:
				inPair = True
				break
		u.inpaire = inPair

	
	if request.user.is_authenticated():
		return render(request,'tennis/staffUser.html',locals())
	return redirect(reverse(home))

def yearsago(years, from_date=None):
    if from_date is None:
        from_date = date.today()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        #assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year-years)

@permission_required('tennis.User')
def viewUser(request,name):
	rankings = Ranking.objects.all()

	use = User.objects.get(username=name)
	today = date.today()
	yearLoop = range(1900,today.year-7)
	birthdate = use.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	terrain = Court.objects.filter(user=use)
	tournoi1 = Pair.objects.filter(user1=use,confirm=True)
	tournoi2 = Pair.objects.filter(user2=use,confirm=True)
	tournoi = list(chain(tournoi1, tournoi2))


	if request.method == "POST":
		email = request.POST['email']
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
		lat = request.POST['lat']
		lng = request.POST['lng']



		#check champs
		if (firstname=="" or lastname=="" or (tel=="" and gsm=="") or street=="" or number=="" or locality=="" or postalcode=="" or birthdate==""):
			errorEdit = "Veuillez remplir tous les champs obligatoires !"
			return render(request,'tennis/profil.html',locals())

		#check format date
		if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$",birthdate) is None:
			errorEdit = "La date de naissance n'a pas le bon format"
			return render(request,'tennis/profil.html',locals())

		#On formate la date
		birthdate2 = birthdate.split("/")
		datenaissance = datetime.datetime(int(birthdate2[2]),int(birthdate2[1]),int(birthdate2[0]))

		use.email = email
		use.save()

		formatedBirthdate = birthdate
		participant = use.participant
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
		participant.classement = Ranking.objects.get(nom=classement)
		participant.latitude = lat
		participant.longitude = lng
		participant.save()

		# Validate classement
		validate_classement_thread(participant)

		successEdit = "Le profil a bien été changé"

	use = User.objects.get(username=name)
	today = date.today()
	yearLoop = range(1900,today.year-7)
	birthdate = use.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	terrain = Court.objects.filter(user=use)
	tournoi1 = Pair.objects.filter(user1=use,confirm=True)
	tournoi2 = Pair.objects.filter(user2=use,confirm=True)
	tournoi = list(chain(tournoi1, tournoi2))

	if request.user.is_authenticated():
		return render(request,'tennis/viewUser.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def validateTerrain(request, id):

	court = Court.objects.get(id=id)
	if request.method == "POST":
		message = request.POST['message']
		if request.POST.__contains__("valide"):
			valide = True
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " valide").save()
		else:
			valide = False
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " non valide").save()

		court.commentaireStaff = message
		court.valide = valide
		court.save()
		successEdit = "Terrain bien édité!"


	if request.user.is_authenticated():
		return render(request,'tennis/validateTerrain.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def terrainPDF(request, id):
    court = Court.objects.get(id=id)
    proprietaire = Participant.objects.get(user=court.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="terrain'+id+'.pdf"'

    PDFTerrain(response, court, proprietaire, request.user.participant)

    return response

def pairPDF(request, id):
	pair = Pair.objects.get(id=id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment;filename="paire'+id+'"'

	PDFPair(response, pair, request.user.participant)

	return response


@permission_required('tennis.Court')
def editTerrainStaff(request, id):
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	court = Court.objects.get(id=id)
	if request.method == "POST":
		if request.POST['action'] == "modifyCourt":
			rue = request.POST['street']
			numero = request.POST['number']
			boite = request.POST['boite']
			postalcode = request.POST['postalcode']
			locality = request.POST['locality']
			lat = request.POST['lat']
			lng = request.POST['lng']
			acces = request.POST['acces']
			matiere = (u''+request.POST['matiere']).encode('utf-8')
			type = request.POST['type']
			etat = (u''+request.POST['etat']).encode('utf-8')
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
			court.matiere=CourtSurface.objects.get(nom=matiere)
			court.type=CourtType.objects.get(nom=type)
			court.dispoDimanche=dispoDimanche
			court.dispoSamedi=dispoSamedi
			court.etat=CourtState.objects.get(nom=etat)
			court.commentaire=commentaire
			court.longitude = lng
			court.latitude = lat
			court.save()
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " edite").save()
			#successEdit = "Terrain "+str(id)+" bien édité!"
			return redirect(reverse(validateTerrain,args={id}))

		if request.POST['action'] == "deleteCourt":
			court.delete()
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " delete").save()
			return redirect(reverse(staffTerrain))
	if request.user.is_authenticated():
		return render(request,'tennis/editTerrainStaff.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def validatePair(request, id):
	pair = Pair.objects.get(id=id)

	allTournoi = Tournoi.objects.all()

	#Check si la paire fait deja partie d'une poule
	noPoule = True
	for elem in Poule.objects.all():
		if pair in elem.paires.all():
			noPoule = False
			break

	info = infoTournoi.objects.all()
	info = info.order_by("edition")[len(info)-1]
	today = info.date
	born = pair.user1.participant.datenaissance
	age1 = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

	born = pair.user2.participant.datenaissance
	age2 = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

	if request.method == "POST":
		if request.POST['action'] == "editPair":
			valid = request.POST['valid']
			paid = request.POST['pay']
			tournoi = request.POST['tournoi']
			title = tournoi
			cat = tournoi
			if "_" in tournoi:
				title = tournoi.split("_")[0]
				cat = tournoi.split("_")[1]

			t = TournoiTitle.objects.get(nom=title)
			c = TournoiCategorie.objects.get(nom=cat)
			new_tournoi = Tournoi.objects.get(titre=t,categorie=c)

			if new_tournoi != pair.tournoi:
				pair.tournoi = new_tournoi
				LogActivity(user=request.user,section="Pair",details="Pair "+id+ " tournoi = "+str(new_tournoi)).save()
			if valid == "Oui":
				valider = True
				if valider != pair.valid:
					LogActivity(user=request.user,section="Pair",details="Pair "+id+ " valide").save()
			else:
				valider = False
				if valider != pair.valid:
					LogActivity(user=request.user,section="Pair",details="Pair "+id+ " non valide").save()
			if paid == "Oui":
				payer = True
				if payer != pair.pay:
					LogActivity(user=request.user,section="Pair",details="Pair "+id+ " paye").save()
			else:
				payer = False
				if payer != pair.pay:
					LogActivity(user=request.user,section="Pair",details="Pair "+id+ " non paye").save()
			pair.valid = valider
			pair.pay = payer
			pair.save()
			return redirect(reverse(validatePair,args={id}))

		if request.POST['action'] == "deletePair":
			pair.delete()
			LogActivity(user=request.user,section="Pair",details="Pair "+id+ " delete").save()
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
			extranot1.append(Extra.objects.get(id=elem.id))

	extra2 = pair.extra2.all()
	extranot2 = list()
	for elem in Ex:
		contained = False
		for el in extra2:
			if elem.id == el.id:
				contained = True
		if contained == False:
			extranot2.append(Extra.objects.get(id=elem.id))

	birthdate1 = pair.user1.participant.datenaissance
	formatedBirthdate1 = birthdate1.strftime('%d/%m/%Y')
	birthdate2 = pair.user2.participant.datenaissance
	formatedBirthdate2 = birthdate2.strftime('%d/%m/%Y')
	if request.user.is_authenticated():
		return render(request,'tennis/validatePair.html',locals())
	return redirect(reverse(home))

def profil(request):
	rankings = Ranking.objects.all()
	today = date.today()
	yearLoop = range(1900,today.year-7)
	birthdate = request.user.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	if request.method == "POST":
		if request.POST['action'] == 'sendMailConfirmationMail':
			# Send email with code to finish registration and validate account
			successSendMail = u"Un email vous a été renvoyé sur votre adresse courante. En cas de non-réception, veuillez revérifier l'adresse enregistrée ci-dessous."
			participant = Participant.objects.get(user = request.user)
			activationObject = UserInWaitOfActivation.objects.get(participant = participant)
			activationObject.dayOfRegistration = datetime.datetime.now()
			activationObject.save()
			link = "http://" + request.get_host() + "/tennis/emailValidation/"
			send_register_confirmation_email(activationObject, participant, link)
			return render(request,'tennis/profil.html',locals())
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
			lat = request.POST['lat']
			lng = request.POST['lng']

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

			formatedBirthdate = birthdate
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
			participant.classement = Ranking.objects.get(nom=classement)
			participant.oldparticipant = oldparticipant
			participant.latitude = lat
			participant.longitude = lng
			participant.save()

			# Validate classement
			validate_classement_thread(participant)

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

def emailValidation(request, key):
	# Read all objects, clean those out of date
	compteToValidate = None
	listOfAll = UserInWaitOfActivation.objects.all()
	for account in listOfAll:
		if account.isStillValid():
			# Keep in memory
			if account.isKeyValid(key):
				compteToValidate = account
		else:
			#account.participant.delete() #TODO ON LE DELETE OU PAS LE PARTICIPANT ?
			account.delete()
	# End of cleaning, if account to validate has been found, validate it and return succes, else failure
	if compteToValidate == None:
		# Failure
		errorValidate = "La cle de validation de compte reçue semble être invalide ou expirée."
	else:
		# Validate participant
		participant = compteToValidate.participant
		participant.isAccountActivated = True
		participant.save()
		#Delete accounr
		compteToValidate.delete()
		#Print succes
		successValidate = "Votre adresse mail est désormais validée, merci de votre coopération."
	return render(request,'tennis/emailValidation.html',locals())

def register(request):
	today = date.today()
	yearLoop = range(1900,today.year-7)
	rankings = Ranking.objects.all()
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
		lat = request.POST['lat']
		lng = request.POST['lng']

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

		#Account creation & redirect
		user = User.objects.create_user(username,email,password)
		user.save()
		#TODO verfied = FALSE
		participant = Participant(user = user,titre=title,nom=lastname,prenom=firstname,rue=street,numero=number,boite=boite,codepostal=postalcode,localite=locality,telephone=tel,fax=fax,gsm=gsm,classement =Ranking.objects.get(nom=classement),oldparticipant = oldparticipant,datenaissance = datenaissance, isClassementVerified = True, isAccountActivated = False, latitude=lat, longitude=lng)
		participant.save()

		# Create UserInWaitOfActivation object to keep track of the activation
		today = datetime.datetime.now()
		key = get_random_string(20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		while len(UserInWaitOfActivation.objects.filter(confirmation_key= key)) > 0 :
			#Key already in user, generate new one
			key = get_random_string(20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
		activationObject = UserInWaitOfActivation(participant = participant, dayOfRegistration = today, confirmation_key= key)
		activationObject.save()
		link = "http://" + request.get_host() + "/tennis/emailValidation/"

		# Verify user classement
		validate_classement_thread(participant)

		# Send email with code to finish registration and validate account
		send_register_confirmation_email(activationObject, participant, link)

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



def printScoreBoard(request, pouleId):
	poule = Poule.objects.get(id=pouleId)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment;filename="poule'+pouleId+'.pdf"'
	PDFPoule(response, poule, request.user)
	return response

@user_passes_test(lambda u: u.groups.filter(name='admin').exists)
def resetDbForNextYear(request):

	listParticipant = Participant.objects.all()
	for participant in listParticipant:
		participant.oldparticipant = False
		participant.save()

	listCourt = Court.objects.all()
	for court in listCourt:
		if len(court.poule_set.all()) > 0:
			court.usedLastYear = True
		else:
			court.usedLastYear = False
		court.dispoSamedi = False
		court.dispoDimanche = False
		court.commentaire = None
		court.commentaireStaff = None
		court.save()

	listPair = Pair.objects.all()
	for pair in listPair:
		user1 = pair.user1
		user2 = pair.user2
		user1.oldparticipant = True
		user2.oldparticipant = True
		user1.save()
		user2.save()

	Extra.objects.all().delete()
	Arbre.objects.all().delete()
	Pair.objects.all().delete()
	Score.objects.all().delete()
	Poule.objects.all().delete()
	LogActivity.objects.all().delete()
	
	i = infoTournoi(prix=20,date=datetime.date(date.today().year+1, 9, 10),addr="Place des Carabiniers, 5, 1030 Bruxelles",edition=43)
	i.save()