#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm
from tennis.models import Extra, Participant,Court, Tournoi,Groupe, Pair, CourtState, CourtSurface, CourtType,LogActivity, UserInWaitOfActivation, Poule,Score, TournoiStatus, PouleStatus,Arbre
from tennis.mail import send_confirmation_email_court_registered, send_confirmation_email_pair_registered, send_email_start_tournament, send_register_confirmation_email, test_send_mail
import re, math
import json
import datetime
from datetime import date
from itertools import chain
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission,Group
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from tennis.pdfdocument import PDFTerrain, PDFPair
from django.template.defaulttags import register



# Create your views here.
def home(request):
	return render(request,'tennis/home.html',locals())

def qcq(request):
	return render(request,'tennis/404.html',locals())

def sponsors(request):
	return render(request,'tennis/sponsors.html',locals())

def resultat(request):
	return render(request,'tennis/resultat.html',locals())

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

	today = date.today()

	for u in Use:
		born = u.participant.datenaissance
		u.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))


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
		allExtras = Extra.objects.all()
		extra1 = pair.extra1.all()
		extra2 = pair.extra2.all()
		totalprice = 40.00
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

def terrain(request):
	if request.user.is_authenticated():
		court = Court.objects.filter(user=request.user)
		return render(request,'tennis/terrain.html',locals())
	return redirect(reverse(home))

def registerTerrain(request):
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	if request.method == "POST":
		rue = request.POST['rue']
		numero = request.POST['numero']
		boite = request.POST['boite']
		postalcode = request.POST['postalcode']
		locality = request.POST['loclity']
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
		court = Court(rue = rue,numero=numero,boite=boite,codepostal=postalcode,localite=locality,acces=acces,matiere=CourtSurface.objects.filter(nom=matiere)[0],type=CourtType.objects.filter(nom=type)[0],dispoDimanche=dispoDimanche,dispoSamedi=dispoSamedi,etat=CourtState.objects.filter(nom=etat)[0],commentaire=commentaire,user = request.user)

		# Send confirmation mail
		##send_confirmation_email_court_registered(Participant.objects.get(user=request.user), court)

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
			court.matiere=CourtSurface.objects.filter(nom=matiere)[0]
			court.type=CourtType.objects.filter(nom=type)[0]
			court.dispoDimanche=dispoDimanche
			court.dispoSamedi=dispoSamedi
			court.etat=CourtState.objects.filter(nom=etat)[0]
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

'''
def staff(request):
	if request.user.is_authenticated():
		return render(request,'tennis/staff.html',locals())
	return redirect(reverse(home))
'''

#TODO permission QUENTIN GUSBIN
def staffTournoi(request):
	if request.user.is_authenticated():
		allTournoi = Tournoi.objects.all()
		for tourn in allTournoi:
			nbrPair = len(Pair.objects.filter(tournoi=tourn))
			tourn.np = nbrPair
			pouleLength = len(Poule.objects.filter(tournoi=tourn))
			tourn.pl = pouleLength
		return render(request,'tennis/staffTournoi.html',locals())
	return redirect(reverse(home))

def pouleTournoi(request,name):
	def getKey(item):
		return item[1]
	
	if request.user.is_authenticated():
		tournoi = Tournoi.objects.get(nom=name)
		poules = Poule.objects.filter(tournoi=tournoi)
		dictionnaire = dict()
		for poule in poules:
			if poule.status == PouleStatus.objects.get(id=2):
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
	tournoi = Tournoi.objects.get(nom=name)
	def getKey(item):
		return item[1]
	if request.method == "POST":
		if request.POST['action'] == "save":
			treeData = request.POST['treeData']
			treeLabel = request.POST['treeLabel']
			if tournoi.arbre is None:
				arbre = Arbre(data = treeData,label = treeLabel)
				arbre.save()
				tournoi.arbre = arbre
				tournoi.save()
			else:
				arbre = tournoi.arbre
				arbre.data = treeData
				arbre.label= treeLabel
				arbre.save()
		elif request.POST['action'] == "deleteTree":
			arbre = tournoi.arbre
			tournoi.arbre = None
			tournoi.save()
			arbre.delete()
						
		
		

	if request.user.is_authenticated():
		
		poules = Poule.objects.filter(tournoi=tournoi)
		dictionnaire = dict()
		allPaires = list()
		for poule in poules:
			if poule.status == PouleStatus.objects.get(id=2):
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
	poule = Poule.objects.get(id=id)
	if request.method == "POST":
		if request.POST['action'] == 'save':
			poule.status = PouleStatus.objects.get(id=1)
			poule.save()
		elif request.POST['action'] == 'saveFinite':
			poule.status = PouleStatus.objects.get(id=2)
			poule.save()
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
	terrains = Court.objects.all()
	tournoi = Tournoi.objects.get(nom=name)
	allPair = Pair.objects.filter(tournoi=tournoi)
	poules = Poule.objects.filter(tournoi=tournoi)
	if request.method == "POST":
		if request.POST['action'] == 'save':
			tournoi.status = TournoiStatus.objects.get(id=1)
			tournoi.save()
		elif request.POST['action'] == 'saveFinite':
			tournoi.status = TournoiStatus.objects.get(id=2)
			tournoi.save()
		terrainsList = request.POST['assignTerrains'].split('-')
		terrainsList.pop()

		leadersList = request.POST['assignLeaders'].split('/')
		leadersList.pop()

		pairspoulesList = request.POST['assignPairPoules'].split('-')
		pairspoulesList.pop()

		i = 0
		j = -1
		pouleDict = {}
		while (i < len(pairspoulesList)):
			if pairspoulesList[i].startswith('[') and pairspoulesList[i].endswith(']'):
				j += 1
				pouleDict[j] = {}
				pouleDict[j]['pairList'] = []
				if terrainsList[j] != '':
					pouleDict[j]['terrain'] = Court.objects.filter(id=terrainsList[j])[0]
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
		Poule.objects.filter(tournoi=tournoi).delete()
		while (i <= j):
			p = Poule(tournoi=tournoi)
			p.status = PouleStatus.objects.get(id=0)
			p.save()
			if 'leader' in pouleDict[i]:
				p.leader = pouleDict[i]['leader']
			if 'terrain' in pouleDict[i]:
				p.court = pouleDict[i]['terrain']
			for pair in pouleDict[i]['pairList']:
				p.paires.add(pair)
			i += 1
			p.save()

		return redirect(reverse(staffTournoi))
	if request.user.is_authenticated():
		dictTerrains = {}
		# TODO : Indiquer les terrains déjà utilisés le jour du tournoi
		for terrain in terrains:
			dictTerrains[terrain.id] = terrain

		listTerrains = list(dictTerrains.values())
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
	#List of Court
	allCourt = Court.objects.all()
	allCourtSurface = CourtSurface.objects.all()
	allCourtType = CourtType.objects.all()
	allCourtState = CourtState.objects.all()
	if request.user.is_authenticated():
		return render(request,'tennis/staffTerrain.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def staffPaire(request):
	#List of Pair
	allPair = Pair.objects.all()
	Tour = Tournoi.objects.all()
	if request.user.is_authenticated():
		return render(request,'tennis/staffPair.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Extra')
def staffExtra(request):

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
			LogActivity(user=request.user,section="Extra",details="Extra "+nom+ " ajoute").save()

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
			LogActivity(user=request.user,section="Extra",details="Extra "+nom+ " modifie").save()
			successEdit = "Extra bien édité!"

		if request.POST['action'] == "deleteExtra":
			id = request.POST['id']
			extra = Extra.objects.filter(id = id)[0]
			extra.delete()
			LogActivity(user=request.user,section="Extra",details="Extra "+extra.nom+ " delete").save()
			successDelete = "Extra bien supprimé!"

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

	if request.method == "POST":

		usernamefield = request.POST['username']
		utilisateur = User.objects.filter(username=usernamefield)[0]
		if request.POST.__contains__("Tournoi des familles"):
			perm = Permission.objects.filter(codename="TournoiDesFamilles")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="TournoiDesFamilles")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("Double mixte"):
			perm = Permission.objects.filter(codename="DoubleMixte")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="DoubleMixte")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("Double hommes"):
			perm = Permission.objects.filter(codename="DoubleHommes")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="DoubleHommes")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("Double femmes"):
			perm = Permission.objects.filter(codename="DoubleFemmes")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="DoubleFemmes")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("court"):
			perm = Permission.objects.filter(codename="Court")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="Court")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("pair"):
			perm = Permission.objects.filter(codename="Pair")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="Pair")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("extra"):
			perm = Permission.objects.filter(codename="Extra")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="Extra")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("user"):
			perm = Permission.objects.filter(codename="User")[0]
			utilisateur.user_permissions.add(perm)
		else:
			perm = Permission.objects.filter(codename="User")[0]
			utilisateur.user_permissions.remove(perm)

		if request.POST.__contains__("perm"):
			group = Group.objects.filter(name="Admin")[0]
			utilisateur.groups.add(group)
		else:
			group = Group.objects.filter(name="Admin")[0]
			utilisateur.groups.remove(group)

		LogActivity(user=request.user,section="Permissions",details="Changed permission of user "+utilisateur.username).save()




	Use = User.objects.all().order_by('username')
	tournoiAll = Tournoi.objects.all()

	for u in Use:
		bd = u.participant.datenaissance
		fb = bd.strftime('%d/%m/%Y')
		u.fb = fb
	if request.user.is_authenticated():
		return render(request,'tennis/staffPerm.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.User')
def staffUser(request):
	Use = User.objects.all().order_by('username')
	today = date.today()
	for u in Use:
		born = u.participant.datenaissance
		u.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
	if request.user.is_authenticated():
		return render(request,'tennis/staffUser.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.User')
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
		return render(request,'tennis/viewUser.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Court')
def validateTerrain(request, id):

	court = Court.objects.filter(id=id)[0]
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
    proprietaire = Participant.objects.filter(user=court.user)[0]
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
	court = Court.objects.filter(id=id)[0]
	if request.method == "POST":
		if request.POST['action'] == "modifyCourt":
			rue = request.POST['rue']
			numero = request.POST['numero']
			boite = request.POST['boite']
			postalcode = request.POST['postalcode']
			locality = request.POST['loclity']
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
			court.matiere=CourtSurface.objects.filter(nom=matiere)[0]
			court.type=CourtType.objects.filter(nom=type)[0]
			court.dispoDimanche=dispoDimanche
			court.dispoSamedi=dispoSamedi
			court.etat=CourtState.objects.filter(nom=etat)[0]
			court.commentaire=commentaire
			court.user = request.user
			court.save()
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " edite").save()
			#successEdit = "Terrain "+str(id)+" bien édité!"
			return redirect(reverse(validateTerrain,args={id}))

		if request.POST['action'] == "deleteCourt":
			#TODO delete terrain staff
			court.delete()
			LogActivity(user=request.user,section="Terrain",details="Terrain "+id+ " delete").save()
			return redirect(reverse(staffTerrain))
	if request.user.is_authenticated():
		return render(request,'tennis/editTerrainStaff.html',locals())
	return redirect(reverse(home))

@permission_required('tennis.Pair')
def validatePair(request, id):
	pair = Pair.objects.filter(id=id)[0]
	if request.method == "POST":
		if request.POST['action'] == "editPair":
			valid = request.POST['valid']
			paid = request.POST['pay']
			if valid == "Oui":
				valider = True
				LogActivity(user=request.user,section="Pair",details="Pair "+id+ " valide").save()
			else:
				valider = False
				LogActivity(user=request.user,section="Pair",details="Pair "+id+ " non valide").save()
			if paid == "Oui":
				payer = True
				LogActivity(user=request.user,section="Pair",details="Pair "+id+ " paye").save()
			else:
				payer = False
				LogActivity(user=request.user,section="Pair",details="Pair "+id+ " non paye").save()
			pair.valid = valider
			pair.pay = payer
			pair.save()

			return redirect(reverse(staffPaire))

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
	yearLoop = range(1900,2015)
	birthdate = request.user.participant.datenaissance
	formatedBirthdate = birthdate.strftime('%d/%m/%Y')
	if request.method == "POST":
		if request.POST['action'] == 'sendMailConfirmationMail':
			# Send email with code to finish registration and validate account
			successSendMail = "Un email vous a ete renvoye sur votre adresse courante. En cas de non - réception veuillez revérifier l'adresse enregistrée ci-dessous."
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
	yearLoop = range(1900,2015)
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

		#Account creation & redirect
		user = User.objects.create_user(username,email,password)
		user.save()
		participant = Participant(user = user,titre=title,nom=lastname,prenom=firstname,rue=street,numero=number,boite=boite,codepostal=postalcode,localite=locality,telephone=tel,fax=fax,gsm=gsm,classement = classement,oldparticipant = oldparticipant,datenaissance = datenaissance, isAccountActivated = False)
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

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
