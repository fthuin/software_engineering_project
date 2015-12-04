#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm
from tennis.models import Extra, Participant, Court, Tournoi, Pair, CourtState, CourtSurface, CourtType, LogActivity, UserInWaitOfActivation, Poule, Score, PouleStatus, Arbre, TournoiStatus, TournoiTitle, TournoiCategorie, infoTournoi, Ranking, Resultat
from tennis.mail import send_confirmation_email_court_registered, send_confirmation_email_pair_registered, send_email_start_tournament, send_register_confirmation_email, test_send_mail, send_contact_mail, send_tournament_invitation_by_mail
from tennis.classement import validate_classement_thread
import re
import math
import copy
import json
import datetime
from datetime import date, timedelta
from itertools import chain
from django.contrib.auth.decorators import permission_required,  user_passes_test
from django.contrib.auth.models import Permission, Group
from django.utils.crypto import get_random_string
from django.http import HttpResponse, HttpResponseRedirect
from tennis.pdfdocument import PDFTerrain, PDFPair, PDFPoule
from django.template.defaulttags import register
from django.db.models import Q
from functools import reduce
from operator import and_, or_
from django.db import connection

db_type = connection.vendor

# Create your views here.


def home(request):
    from views_helper import home as homepage
    return homepage.view(request)


def qcq(request):
    return render(request, '404.html', {})


def sponsors(request):
    return render(request, 'sponsors.html', {})


def allResult(request):
    info = infoTournoi.objects.all()
    return render(request, 'resultatAll.html', locals())


def resultat(request, id):
    info = infoTournoi.objects.get(edition=id)
    # Resultat du tournoi des familles
    ti = TournoiTitle.objects.get(nom="Tournoi des familles")
    famille = info.resultats.filter(tournoi__titre=ti)
    if len(famille) > 0:
        famille = famille[0]

    # Resultat du Double mixte
    ti = TournoiTitle.objects.get(nom="Double mixte")
    mixte = info.resultats.filter(tournoi__titre=ti)

    # Resultat du Double femmes
    ti = TournoiTitle.objects.get(nom="Double femmes")
    femmes = info.resultats.filter(tournoi__titre=ti)

    # Resultat du Double hommes
    ti = TournoiTitle.objects.get(nom="Double hommes")
    hommes = info.resultats.filter(tournoi__titre=ti)

    ti = None

    return render(request, 'resultat.html', locals())


def contact(request):
    if request.method == "POST":
        if request.POST['action'] == "sendConcactMail":
            subject = request.POST['subject']
            email = request.POST['email']
            message = request.POST['message']
            if send_contact_mail(email, subject, message):
                successSendMail = u"Votre message a bien été envoyé"
            else:
                echecSendMail = u"Une erreur s'est produite lors de l'envois de votre message,\nle problème a été signaler au staff et sera résolu dans les plus bref délais. Désole de l'inconvénience, réessayer dans quelques heures"
    return render(request, 'contact.html', locals())


def tournoi(request):
    from views_helper import tournoi as tournoipage
    return tournoipage.view(request)


def inscriptionTournoi(request):
    from views_helper import inscription_tournoi as inscriptionpage
    return inscriptionpage.view(request)


def confirmPair(request, id):
    pair = Pair.objects.filter(id=id)
    if len(pair) < 1:
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
            # TODO Envoyer mail a l'user 1 pour lui dire que son pote veut pas
            # de lui
    if request.user.is_authenticated():
        # TODO check si il peut confirmer cette pair

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

        return render(request, 'confirmPair.html', locals())
    return redirect(reverse(home))


def cancelPair(request, id):
    pair = Pair.objects.filter(id=id)
    if len(pair) < 1:
        return redirect(reverse(tournoi))
    pair = Pair.objects.get(id=id)
    if pair.user1 != request.user:
        return redirect(reverse(tournoi))
    if request.method == "POST":
        # TODO check si il peut annuler cette pair
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

        return render(request, 'cancelPair.html', locals())
    return redirect(reverse(home))


def viewPair(request, id):
    if request.method == "POST":
        pair = Pair.objects.filter(id=id)
        pair.delete()
        return redirect(reverse(tournoi))
    pair = Pair.objects.filter(id=id)
    if len(pair) < 1:
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
        return render(request, 'viewPair.html', locals())
    return redirect(reverse(home))


def payPair(request, id):
    pair = Pair.objects.filter(id=id)
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    prix = info.prix
    if len(pair) < 1:
        return redirect(reverse(tournoi))
    pair = Pair.objects.get(id=id)
    if pair.user1 != request.user and pair.user2 != request.user:
        return redirect(reverse(tournoi))
    if request.user.is_authenticated():
        # TODO check si il peut payer cette pair
        allExtras = Extra.objects.all()
        extra1 = pair.extra1.all()
        extra2 = pair.extra2.all()
        totalprice = 2 * prix
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
            totalprice += float(count * extra.prix)

        return render(request, 'payPair.html', locals())
    return redirect(reverse(home))


def enterScore(request, id):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    poule = Poule.objects.get(id=id)
    if request.method == "POST":
        poule.status = PouleStatus.objects.get(numero=1)
        poule.save()
        poule.score.all().delete()
        pairList = poule.paires.all()
        dictionnaire = dict()
        for id1 in pairList:
            for id2 in pairList:
                if((str(id1.id) + "-" + str(id2.id) in dictionnaire) or (str(id2.id) + "-" + str(id1.id) in dictionnaire) or (id1 == id2)):
                    pass
                else:
                    dictionnaire[str(id1.id) + "-" + str(id2.id)] = True
                    dictionnaire[str(id2.id) + "-" + str(id1.id)] = True

                    if (is_number(request.POST[str(id1.id) + "-" + str(id2.id)]) and is_number(request.POST[str(id2.id) + "-" + str(id1.id)])):
                        score = Score(paire1=id1, paire2=id2, point1=int(request.POST[str(
                            id1.id) + "-" + str(id2.id)]), point2=int(request.POST[str(id2.id) + "-" + str(id1.id)]))
                        score.save()
                        poule.score.add(score)

        if len(poule.score.all()) == 0:
            poule.status = PouleStatus.objects.get(numero=0)
            poule.save()
        return redirect(reverse(tournoi))

    if request.user.is_authenticated():
        scoreList = poule.score.all()
        scoreValues = ""
        for sco in scoreList:
            scoreValues = scoreValues + repr(sco.paire1.id) + "-" + repr(sco.paire2.id) + "," + repr(
                sco.point1) + "." + repr(sco.paire2.id) + "-" + repr(sco.paire1.id) + "," + repr(sco.point2) + "."
        scoreValues = scoreValues[:-1]
        return render(request, 'playerScore.html', locals())
    return redirect(reverse(home))


def terrain(request):
    if request.user.is_authenticated():
        if Participant.objects.get(user=request.user).isAccountActivated:
            court = Court.objects.filter(user=request.user)
            return render(request, 'terrain.html', locals())
        else:
            return render(request, 'terrainUserNotValidated.html', locals())
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

        if (rue == "" or numero == "" or postalcode == "" or locality == "" or matiere == "" or type == "" or etat == ""):
            errorAdd = "Veuillez remplir tous les champs obligatoires !"
            return render(request, 'registerTerrain.html', locals())

        # Create court object
        court = Court(rue=rue, numero=numero, boite=boite, codepostal=postalcode, localite=locality, acces=acces, matiere=CourtSurface.objects.get(nom=matiere), type=CourtType.objects.get(
            nom=type), dispoDimanche=dispoDimanche, dispoSamedi=dispoSamedi, etat=CourtState.objects.get(nom=etat), commentaire=commentaire, user=request.user, latitude=lat, longitude=lng)

        # Send confirmation mail
        send_confirmation_email_court_registered(
            Participant.objects.get(user=request.user), court)

        court.save()
        return redirect(reverse(terrain))

    if request.user.is_authenticated():
        return render(request, 'registerTerrain.html', locals())
    return redirect(reverse(home))


def editTerrain(request, id):
    allCourtSurface = CourtSurface.objects.all()
    allCourtType = CourtType.objects.all()
    allCourtState = CourtState.objects.all()
    court = Court.objects.filter(id=id)

    if len(court) < 1:
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

            if (rue == "" or numero == "" or postalcode == "" or locality == "" or matiere == "" or type == "" or etat == ""):
                errorAdd = "Veuillez remplir tous les champs obligatoires !"
                return render(request, 'registerTerrain.html', locals())

            court.rue = rue
            court.numero = numero
            court.boite = boite
            court.codepostal = postalcode
            court.localite = locality
            court.acces = acces
            court.matiere = CourtSurface.objects.get(nom=matiere)
            court.type = CourtType.objects.get(nom=type)
            court.dispoDimanche = dispoDimanche
            court.dispoSamedi = dispoSamedi
            court.etat = CourtState.objects.get(nom=etat)
            court.commentaire = commentaire
            court.user = request.user
            court.latitude = lat
            court.longitude = lng
            court.save()
            successEdit = "Terrain " + str(id) + " bien édité!"
            return redirect(reverse(terrain))

        if request.POST['action'] == "deleteCourt":

            court.delete()
            return redirect(reverse(terrain))

    if request.user.is_authenticated():

        if request.user == court.user:
            return render(request, 'editTerrain.html', locals())
    return redirect(reverse(home))

# TODO permission QUENTIN GUSBIN


def staffTournoi(request):
    if request.user.is_authenticated():
        allTitre = TournoiTitle.objects.all()
        allTournoi = Tournoi.objects.all()
        for tourn in allTournoi:
            nbrPair = len(Pair.objects.filter(tournoi=tourn, valid=True))
            tourn.np = nbrPair
            pouleLength = len(Poule.objects.filter(tournoi=tourn))
            tourn.pl = pouleLength
        return render(request, 'staffTournoi.html', locals())
    return redirect(reverse(home))


def pouleTournoi(request, name):
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
        tournoi = Tournoi.objects.get(titre=ti, categorie=ca)
        s = TournoiStatus.objects.get(numero=1)
        tournoi.status = s
        a = tournoi.arbre
        tournoi.arbre = None
        tournoi.save()
        LogActivity(user=request.user, section="Poules",
                    details="Suppressions des poules du tournoi : " + tournoi.nom()).save()
        return redirect(reverse(generatePool, args={name}))

    if request.user.is_authenticated():
        title = name
        cat = name
        if "_" in name:
            title = name.split("_")[0]
            cat = name.split("_")[1]
        ti = TournoiTitle.objects.get(nom=title)
        ca = TournoiCategorie.objects.get(nom=cat)
        tournoi = Tournoi.objects.get(titre=ti, categorie=ca)
        poules = Poule.objects.filter(tournoi=tournoi)
        dictionnaire = dict()
        x = 0
        for poule in poules:
            if x % 2 == 0:
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
                    dico[score.paire1.id] = dico[
                        score.paire1.id] + score.point1
                    dico[score.paire2.id] = dico[
                        score.paire2.id] + score.point2
                liste = list()
                for key, value in dico.items():
                    liste.append((key, value))
                liste = sorted(liste, key=getKey, reverse=True)
                dictionnaire[poule.id] = liste
                poule.SortedPair = list()
                for pairID, sc in liste:
                    pai = Pair.objects.get(id=pairID)
                    pai.score = sc
                    poule.SortedPair.append(pai)

        return render(request, 'pouleTournoi.html', locals())
    return redirect(reverse(home))

# TODO permissions QUENTIN GUSBIN


def knockOff(request, name):
    from views_helper import knockoff
    return knockoff.view(request, name)

# TODO permission QUENTIN GUSBIN


def pouleViewScore(request, id):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    poule = Poule.objects.get(id=id)
    if request.method == "POST":
        poule.score.all().delete()
        poule.status = PouleStatus.objects.get(numero=0)
        poule.save()
        return redirect(reverse(pouleTournoi, args={poule.tournoi.nom()}))

    if request.user.is_authenticated():
        scoreList = poule.score.all()
        scoreValues = ""
        for sco in scoreList:
            scoreValues = scoreValues + repr(sco.paire1.id) + "-" + repr(sco.paire2.id) + "," + repr(
                sco.point1) + "." + repr(sco.paire2.id) + "-" + repr(sco.paire1.id) + "," + repr(sco.point2) + "."
        scoreValues = scoreValues[:-1]
        return render(request, 'viewScore.html', locals())
    return redirect(reverse(home))


# TODO permission QUENTIN GUSBIN
def pouleScore(request, id):
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
            # Check si toutes les poules sont finite
            valid = True
            for elem in Poule.objects.filter(tournoi=poule.tournoi):
                if elem.status.numero != 2:
                    valid = False
                    break
            if valid:
                t = poule.tournoi
                t.status = TournoiStatus.objects.get(numero=3)
                t.save()
            LogActivity(user=request.user, section="Tournoi",
                        details="Mise a jour des point de la poule " + id + " dans le tournoi ").save()
        poule.score.all().delete()
        pairList = poule.paires.all()
        dictionnaire = dict()
        for id1 in pairList:
            for id2 in pairList:
                if((str(id1.id) + "-" + str(id2.id) in dictionnaire) or (str(id2.id) + "-" + str(id1.id) in dictionnaire) or (id1 == id2)):
                    pass
                else:
                    dictionnaire[str(id1.id) + "-" + str(id2.id)] = True
                    dictionnaire[str(id2.id) + "-" + str(id1.id)] = True

                    if (is_number(request.POST[str(id1.id) + "-" + str(id2.id)]) and is_number(request.POST[str(id2.id) + "-" + str(id1.id)])):
                        score = Score(paire1=id1, paire2=id2, point1=int(request.POST[str(
                            id1.id) + "-" + str(id2.id)]), point2=int(request.POST[str(id2.id) + "-" + str(id1.id)]))
                        score.save()
                        poule.score.add(score)

        if len(poule.score.all()) == 0:
            poule.status = PouleStatus.objects.get(numero=0)
            poule.save()

        if request.POST['action'] == 'save':
            return redirect(reverse(pouleScore, args={id}))
        elif request.POST['action'] == 'saveFinite':
            return redirect(reverse(pouleTournoi, args={poule.tournoi.nom()}))

        return redirect(reverse(staffTournoi))
    if request.user.is_authenticated():
        scoreList = poule.score.all()
        scoreValues = ""
        for sco in scoreList:
            scoreValues = scoreValues + repr(sco.paire1.id) + "-" + repr(sco.paire2.id) + "," + repr(
                sco.point1) + "." + repr(sco.paire2.id) + "-" + repr(sco.paire1.id) + "," + repr(sco.point2) + "."
        scoreValues = scoreValues[:-1]
        return render(request, 'pouleScore.html', locals())
    return redirect(reverse(home))

# TODO permission QUENTIN GUSBIN


def generatePool(request, name):
    from views_helper import generation_poules
    return generation_poules.view(request, name)


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

    # Recherche
    if recherche != "":
        if db_type == "postgresql":
            allCourt = allCourt.filter(
                Q(id__icontains=recherche) |
                Q(user__username__unaccent__icontains=recherche) |
                Q(user__participant__nom__unaccent__icontains=recherche) |
                Q(user__participant__prenom__unaccent__icontains=recherche) |
                Q(numero__icontains=recherche) |
                Q(rue__unaccent__icontains=recherche) |
                Q(localite__unaccent__icontains=recherche) |
                Q(codepostal__icontains=recherche))
        else:
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
        # samedi
        if dispo == "1":
            allCourt = allCourt.filter(dispoSamedi=True)
        # dimanche
        elif dispo == "2":
            allCourt = allCourt.filter(dispoDimanche=True)
        # samedi et dimanche
        else:
            allCourt = allCourt.filter(dispoSamedi=True, dispoDimanche=True)

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
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    allCourt = allCourt[debut - 1:fin]

    for court in allCourt:
        if len(court.poule_set.all()) > 0:
            court.used = True
        else:
            court.used = False

    allCourtSurface = CourtSurface.objects.all()
    allCourtType = CourtType.objects.all()
    allCourtState = CourtState.objects.all()
    if request.user.is_authenticated():
        return render(request, 'staffTerrain.html', locals())
    return redirect(reverse(home))


@permission_required('tennis.Pair')
def staffPaire(request):
    from views_helper import staff_paires
    return staff_paires.view(request)


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
    info = info.order_by("edition")[len(info) - 1]
    prix_inscription = info.prix
    date_inscription = info.date
    formated_date = date_inscription.strftime('%d/%m/%Y')
    yearLoop = range(date.today().year, date.today().year + 5)
    isAdmin = request.user.groups.filter(name="Admin").exists()

    if request.method == "POST":
        if request.POST['action'] == "cleanDb":
            resetDbForNextYear(request)

        if request.POST['action'] == "modifyInfoTournoi":
            prixTournoi = request.POST['prixInscription'].strip()
            dateInfoTournoi = request.POST['birthdate'].strip()

            info = infoTournoi.objects.all()
            info = info.order_by("edition")[len(info) - 1]
            prixTournoi = prixTournoi.replace(",", ".")
            if(float(prixTournoi) >= 0.0):
                info.prix = prixTournoi
                LogActivity(user=request.user, section="InfoTournoi",
                            details=u"Prix du tournoi modifié").save()
            else:
                errorInfoPrix = "Le prix doit etre plus grand ou égale a zéro"

            splitedDateInfoTournoi = dateInfoTournoi.split("/")
            datetoEnreg = datetime.datetime(int(splitedDateInfoTournoi[2]), int(
                splitedDateInfoTournoi[1]), int(splitedDateInfoTournoi[0]))
            now = datetime.datetime.now()
            if(now < datetoEnreg):
                info.date = datetoEnreg
                LogActivity(user=request.user, section="InfoTournoi",
                            details=u"Date du tournoi modifiée").save()
            else:
                errorInfoDate = "La date doit etre plus tard que maintenant"

            info.save()
            info = infoTournoi.objects.all()
            info = info.order_by("edition")[len(info) - 1]
            prix_inscription = info.prix
            date_inscription = info.date
            formated_date = date_inscription.strftime('%d/%m/%Y')
            return render(request, 'staffExtra.html', locals())

        if request.POST['action'] == "addExtra":
            nom = request.POST['name'].strip()
            prix = request.POST['price'].strip()
            message = request.POST['message'].strip()

            if nom == "":
                errorAdd = "Veuillez rajouter un nom à l'extra!"
                return render(request, 'staffExtra.html', locals())

            if not is_number(prix):
                prix = prix.replace(",", ".")
                if not is_number(prix):
                    errorAdd = "Le prix n'a pas le bon format"
                    return render(request, 'staffExtra.html', locals())

            extra = Extra(nom=nom, prix=prix, commentaires=message)
            extra.save()
            LogActivity(user=request.user, section="Extra",
                        details=u"Extra " + nom + u" ajouté").save()

            successAdd = u"Extra " + nom + u" bien ajouté!"

        if request.POST['action'] == "modifyExtra":
            id = request.POST['id']
            nom = request.POST['name']
            prix = request.POST['price']
            message = request.POST['message']

            extra = Extra.objects.get(id=id)

            if nom == "":
                errorEdit = u"Veuillez rajouter un nom à l'extra!"
                return render(request, 'staffExtra.html', locals())

            if not is_number(prix):
                prix = prix.replace(",", ".")
                if not is_number(prix):
                    errorEdit = u"Le prix n'a pas le bon format"
                    return render(request, 'staffExtra.html', locals())

            extra.nom = nom
            extra.prix = prix
            extra.commentaires = message
            extra.save()
            LogActivity(user=request.user, section="Extra",
                        details=u"Extra " + nom + u" modifié").save()
            successEdit = u"Extra " + nom + u" bien modifié !"

        if request.POST['action'] == "deleteExtra":
            id = request.POST['id']
            extra = Extra.objects.get(id=id)
            extra.delete()
            LogActivity(user=request.user, section="Extra",
                        details=u"Extra " + extra.nom + u" delete").save()
            successDelete = u"Extra bien supprimé!"

    extras = Extra.objects.all()

    for e in extras:
        a = len(Extra.objects.filter(id=e.id, extra1__valid=True)) + \
            len(Extra.objects.filter(id=e.id, extra2__valid=True))
        e.count = a

    if request.user.is_authenticated():
        return render(request, 'staffExtra.html', locals())
    return redirect(reverse(home))


def staffLog(request):
    logs = LogActivity.objects.order_by('-date')
    if request.user.is_authenticated():
        return render(request, 'staffLog.html', locals())
    return redirect(reverse(home))


@permission_required('tennis.Droit')
# TODO permission droit
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

            if staff:
                group = Group.objects.get(name="staff")
                utilisateur.groups.add(group)
            else:
                group = Group.objects.get(name="staff")
                utilisateur.groups.remove(group)

            LogActivity(user=request.user, section="Permissions",
                        details="Changed permission of user " + utilisateur.username).save()

    Use = User.objects.all().order_by('username')

    if recherche != "":
        if db_type == "postgresql":
            Use = Use.filter(
                Q(username__unaccent__icontains=recherche) |
                Q(participant__nom__unaccent__icontains=recherche) |
                Q(participant__prenom__unaccent__icontains=recherche))
        else:
            Use = Use.filter(
                Q(username__icontains=recherche) |
                Q(participant__nom__icontains=recherche) |
                Q(participant__prenom__icontains=recherche))

    Use = Use.order_by("username")
    length = len(Use)
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    Use = Use[debut - 1:fin]
    tournoiAll = TournoiTitle.objects.all()

    for u in Use:
        bd = u.participant.datenaissance
        fb = bd.strftime('%d/%m/%Y')
        u.fb = fb
    if request.user.is_authenticated():
        return render(request, 'staffPerm.html', locals())
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

    # recherche sexe
    if(sexe != ""):
        Use = Use.filter(participant__titre=sexe)
    # recherche veteran
    if(veteran != ""):
        if(veteran == "True"):
            Use = Use.filter(participant__oldparticipant=True)
        else:
            Use = Use.filter(participant__oldparticipant=False)

    date_min = yearsago(age_min)
    date_max = yearsago(age_max)

    # Recherche age min
    Use = Use.filter(participant__datenaissance__lte=date_min)

    # Recherceh age max
    Use = Use.filter(participant__datenaissance__gte=date_max)

    #recherche in paire
    if(in_paire != ""):
        if in_paire == "True":
            Use = Use.filter(Q(user1__confirm=True) | Q(user2__confirm=True))
        else:
            Use = Use.filter(
                ~(Q(user1__confirm=True) | Q(user2__confirm=True)))

    # recherche firld
    if(recherche != ""):
        if db_type == "postgresql":
            Use = Use.filter(Q(username__unaccent__icontains=recherche) | Q(
                participant__nom__unaccent__icontains=recherche) | Q(participant__prenom__unaccent__icontains=recherche))
        else:
            Use = Use.filter(Q(username__icontains=recherche) | Q(
                participant__nom__icontains=recherche) | Q(participant__prenom__icontains=recherche))

    Use = Use.order_by("username")
    length = len(Use)
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    Use = Use[debut - 1:fin]

    ageRange = range(0, 100)

    today = date.today()
    for u in Use:
        born = u.participant.datenaissance
        u.age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
        u1_list = u.user1.all()
        u2_list = u.user2.all()
        inPair = False
        for p in u1_list or u2_list:
            if p.confirm:
                inPair = True
                break
        u.inpaire = inPair

    if request.user.is_authenticated():
        return render(request, 'staffUser.html', locals())
    return redirect(reverse(home))


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = date.today()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        # assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year - years)

# Idealement visible que aux membre du groupe staff Todo?


def viewUser(request, name):
    rankings = Ranking.objects.all()

    use = User.objects.get(username=name)
    today = date.today()
    yearLoop = range(1900, today.year - 7)
    birthdate = use.participant.datenaissance
    formatedBirthdate = birthdate.strftime('%d/%m/%Y')
    terrain = Court.objects.filter(user=use)
    tournoi1 = Pair.objects.filter(user1=use, confirm=True)
    tournoi2 = Pair.objects.filter(user2=use, confirm=True)
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

        # check champs
        if (firstname == "" or lastname == "" or (tel == "" and gsm == "") or street == "" or number == "" or locality == "" or postalcode == "" or birthdate == ""):
            errorEdit = "Veuillez remplir tous les champs obligatoires !"
            return render(request, 'profil.html', locals())

        # check format date
        if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$", birthdate) is None:
            errorEdit = "La date de naissance n'a pas le bon format"
            return render(request, 'profil.html', locals())

        # On formate la date
        birthdate2 = birthdate.split("/")
        datenaissance = datetime.datetime(
            int(birthdate2[2]), int(birthdate2[1]), int(birthdate2[0]))

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
    yearLoop = range(1900, today.year - 7)
    birthdate = use.participant.datenaissance
    formatedBirthdate = birthdate.strftime('%d/%m/%Y')
    terrain = Court.objects.filter(user=use)
    tournoi1 = Pair.objects.filter(user1=use, confirm=True)
    tournoi2 = Pair.objects.filter(user2=use, confirm=True)
    tournoi = list(chain(tournoi1, tournoi2))

    if request.user.is_authenticated():
        return render(request, 'viewUser.html', locals())
    return redirect(reverse(home))


@permission_required('tennis.Court')
def validateTerrain(request, id):

    court = Court.objects.get(id=id)
    if request.method == "POST":
        message = request.POST['message']
        if request.POST.__contains__("valide"):
            valide = True
            LogActivity(user=request.user, section="Terrain",
                        details="Terrain " + id + " valide").save()
        else:
            valide = False
            LogActivity(user=request.user, section="Terrain",
                        details="Terrain " + id + " non valide").save()

        court.commentaireStaff = message
        court.valide = valide
        court.save()
        successEdit = "Terrain bien édité!"

    if request.user.is_authenticated():
        return render(request, 'validateTerrain.html', locals())
    return redirect(reverse(home))


@permission_required('tennis.Court')
def terrainPDF(request, id):
    court = Court.objects.get(id=id)
    proprietaire = Participant.objects.get(user=court.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="terrain' + id + '.pdf"'

    PDFTerrain(response, court, proprietaire, request.user.participant)

    return response


def pairPDF(request, id):
    pair = Pair.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="paire' + id + '"'

    PDFPair(response, pair, request.user.participant)

    return response


@permission_required('tennis.Court')
def editTerrainStaff(request, id):
    from views_helper import staff_terrain_edition
    return staff_terrain_edition.view(request, id)


@permission_required('tennis.Pair')
def validatePair(request, id):
    from views_helper import staff_validation_paire
    return staff_validation_paire.view(request, id)


def profil(request):
    from views_helper import profil as profilpage
    return profilpage.view(request)


def connect(request):
    from views_helper import connexion
    return connexion.view(request)


def deconnect(request):
    logout(request)
    return redirect(reverse(home))


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
            # account.participant.delete() #TODO ON LE DELETE OU PAS LE
            # PARTICIPANT ?
            account.delete()
    # End of cleaning, if account to validate has been found, validate it and
    # return succes, else failure
    if compteToValidate == None:
        # Failure
        errorValidate = "La cle de validation de compte reçue semble être invalide ou expirée."
    else:
        # Validate participant
        participant = compteToValidate.participant
        participant.isAccountActivated = True
        participant.save()
        # Delete accounr
        compteToValidate.delete()
        # Print succes
        successValidate = "Votre adresse mail est désormais validée, merci de votre coopération."
    return render(request, 'emailValidation.html', locals())


def register(request):
    from views_helper import register as registerpage
    return registerpage.view(request)


def group(request):
    return render(request, 'group.html', locals())


def recover(request):
    return render(request, 'recover.html', locals())


def printScoreBoard(request, pouleId):
    poule = Poule.objects.get(id=pouleId)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="poule' + \
        pouleId + '.pdf"'
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

    i = infoTournoi(prix=20, date=datetime.date(date.today().year + 1, 9, 10),
                    addr="Place des Carabiniers, 5, 1030 Bruxelles", edition=43)
    i.save()
