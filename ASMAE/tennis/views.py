#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ce fichier contient les méthodes qui créent toutes les views pour le site,
toutes les requêtes HTTP au serveur sont traitées ici.
'''
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from tennis.forms import LoginForm
from tennis.models import Extra, Participant, Court, Tournoi, Pair, CourtState, CourtSurface, CourtType, LogActivity, UserInWaitOfActivation, Poule, Score, PouleStatus, Arbre, TournoiStatus, TournoiTitle, TournoiCategorie, infoTournoi, Ranking, Resultat
from tennis.mail import send_confirmation_email_court_registered, send_confirmation_email_pair_registered, send_email_start_tournament, send_register_confirmation_email, test_send_mail, send_contact_mail, send_tournament_invitation_by_mail
from tennis.classement import validate_classement_thread
from datetime import date
import datetime
from django.contrib.auth.decorators import permission_required,  user_passes_test
from django.contrib.auth.models import Permission, Group
from django.http import HttpResponse
from tennis.pdfdocument import PDFTerrain, PDFPair, PDFPoule, PDF_all_poules
from django.db.models import Q
from functools import reduce
from django.db import connection

db_type = connection.vendor

FinalPermsDict = {"Double hommes":"DoubleHommes","Tournoi des familles":"TournoiDesFamilles","Double mixte":"DoubleMixte","Double femmes":"DoubleFemmes"}


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
    from views_helper import resultats
    return resultats.view(request, id)


def contact(request):
    from views_helper import contact as contactpage
    return contactpage.view(request)


def tournoi(request):
    from views_helper import tournoi as tournoipage
    return tournoipage.view(request)


def inscriptionTournoi(request):
    from views_helper import inscription_tournoi as inscriptionpage
    return inscriptionpage.view(request)


def confirmPair(request, id):
    from views_helper import user_paire_accord
    return user_paire_accord.view(request, id)


def cancelPair(request, id):
    from views_helper import user_paire_demande
    return user_paire_demande.view(request, id)


def viewPair(request, id):
    from views_helper import user_paire
    return user_paire.view(request, id)


def payPair(request, id):
    from views_helper import user_pair_paiement
    return user_pair_paiement.view(request, id)


def enterScore(request, id):
    from views_helper import user_score_enter
    return user_score_enter.view(request, id)


def terrain(request):
    if request.user.is_authenticated():
        if Participant.objects.get(user=request.user).isAccountActivated:
            court = Court.objects.filter(user=request.user)
            return render(request, 'terrain.html', locals())
        else:
            return render(request, 'terrainUserNotValidated.html', locals())
    return redirect(reverse(home))


def registerTerrain(request):
    from views_helper import user_ajouter_terrain
    return user_ajouter_terrain.view(request)


def editTerrain(request, id):
    from views_helper import user_terrain_modification
    return user_terrain_modification.view(request, id)

def staffTournoi(request):
    userPermissions = request.user.user_permissions.all()
    userGroups = request.user.groups.all()
    #On vérifie que l'utilisateur a au moins une permission de tournoi ou fait partie du groupe admin
    if len(userPermissions.filter(codename="DoubleHommes")) > 0 or len(userPermissions.filter(codename="DoubleFemmes")) > 0 or len(userPermissions.filter(codename="DoubleMixte")) > 0 or len(userPermissions.filter(codename="TournoiDesFamilles")) > 0 or len(userGroups.filter(name="Admin")) > 0:
        if request.user.is_authenticated():
            allTitre = TournoiTitle.objects.all()
            allTournoi = Tournoi.objects.all()
            logs_tournois = LogActivity.objects.filter(section="Tournoi")
            logs_tournois = logs_tournois | LogActivity.objects.filter(section="Poules")
            logs_tournois = logs_tournois.order_by('-date')[:15]
            for tourn in allTournoi:
                nbrPair = len(Pair.objects.filter(tournoi=tourn, valid=True))
                tourn.np = nbrPair
                pouleLength = len(Poule.objects.filter(tournoi=tourn))
                tourn.pl = pouleLength
            return render(request, 'staffTournoi.html', locals())
    return redirect(reverse(home))


def pouleTournoi(request, name):
    nomTournoi = name.split("_")
    if(len(request.user.user_permissions.filter(codename=FinalPermsDict[nomTournoi[0]])) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
        from views_helper import staff_tournoi_poules_resume
        return staff_tournoi_poules_resume.view(request, name)
    return redirect(reverse(home))




def knockOff(request, name):
    nomTournoi = name.split("_")
    if(len(request.user.user_permissions.filter(codename=FinalPermsDict[nomTournoi[0]])) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
        from views_helper import knockoff
        return knockoff.view(request, name)
    return redirect(reverse(home))

# TODO permission QUENTIN GUSBIN


def pouleViewScore(request, id):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    poule = Poule.objects.get(id=id)
    tournoiName = poule.tournoi
    if(len(request.user.user_permissions.filter(codename=FinalPermsDict[tournoiName.titre.nom])) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
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



def pouleScore(request, id):
    poule = Poule.objects.get(id=id)
    tournoiName = poule.tournoi
    if(len(request.user.user_permissions.filter(codename=FinalPermsDict[tournoiName.titre.nom])) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
        from views_helper import staff_poule_score_encode
        return staff_poule_score_encode.view(request, id)
    return redirect(reverse(home))

def generatePool(request, name):
    
    nomTournoi = name.split("_")
    if(len(request.user.user_permissions.filter(codename=FinalPermsDict[nomTournoi[0]])) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
        from views_helper import poules_generation
        return poules_generation.view(request, name)
    return redirect(reverse(home))


@permission_required('tennis.Court')
def staffTerrain(request):
    from views_helper import staff_terrains
    return staff_terrains.view(request)


@permission_required('tennis.Pair')
def staffPaire(request):
    from views_helper import staff_paires
    return staff_paires.view(request)


@permission_required('tennis.Extra')
def staffExtra(request):
    from views_helper import staff_inscriptions
    return staff_inscriptions.view(request)


def staffLog(request):
    if(len(request.user.groups.filter(name="staff")) > 0 or len(request.user.groups.filter(name="Admin")) > 0):
        from views_helper import staff_historique
        return staff_historique.view(request)
    return redirect(reverse(home))


@permission_required('tennis.Droit')
def staffPerm(request):
    from views_helper import staff_permissions
    return staff_permissions.view(request)


@permission_required('tennis.User')
def staffUser(request):
    from views_helper import staff_users
    return staff_users.view(request)


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
    from views_helper import staff_user_edition
    return staff_user_edition.view(request, name)


@permission_required('tennis.Court')
def validateTerrain(request, id):
    from views_helper import staff_terrain_validation
    return staff_terrain_validation.view(request, id)


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
    response['Content-Disposition'] = 'attachment;filename="paire' + id + '.pdf"'

    PDFPair(response, pair, request.user.participant)

    return response


@permission_required('tennis.Court')
def editTerrainStaff(request, id):
    from views_helper import staff_terrain_edition
    return staff_terrain_edition.view(request, id)


@permission_required('tennis.Pair')
def validatePair(request, id):
    from views_helper import staff_paire_validation
    return staff_paire_validation.view(request, id)


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
			# Delete participant, user and account
			account.participant.user.delete()
			account.participant.delete()
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

    #Tous les participants set a no old participant
    listParticipant = Participant.objects.all()
    for participant in listParticipant:
        participant.oldparticipant = False
        participant.save()

    #Reset des court
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

    #Mise a jours des old participant sur les utilisateurs
    listPair = Pair.objects.all()
    for pair in listPair:
        user1 = pair.user1
        user2 = pair.user2
        user1.oldparticipant = True
        user2.oldparticipant = True
        user1.save()
        user2.save()

    #Suppressions des extras
    Extra.objects.all().delete()
    #Suppressions des arbres
    Arbre.objects.all().delete()
    #Suppressions des paires
    Pair.objects.all().delete()
    #Suppressions des scores
    Score.objects.all().delete()
    #Suppressions des poules
    Poule.objects.all().delete()
    #Suppressions du log activity
    #LogActivity.objects.all().delete()

    #Status des tournois
    for elem in Tournoi.objects.all():
        elem.status = TournoiStatus.objects.get(numero=0)
        elem.save()

    #Ajout d'une nouvelle edition
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    ed = info.edition
    i = infoTournoi(prix=20, date=datetime.date(date.today().year + 1, 9, 10),
                    addr="Place des Carabiniers, 5, 1030 Bruxelles", edition=ed+1)
    i.save()

def knockoff_print(request, name):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="poules ' + \
        name + '.pdf"'
    title = name
    cat = name
    if "_" in name:
        title = name.split("_")[0]
        cat = name.split("_")[1]
    ti = TournoiTitle.objects.get(nom=title)
    ca = TournoiCategorie.objects.get(nom=cat)
    tournoi = Tournoi.objects.get(titre=ti, categorie=ca)
    all_poules = Poule.objects.filter(tournoi=tournoi)
    PDF_all_poules(response, all_poules, request.user)
    return response
