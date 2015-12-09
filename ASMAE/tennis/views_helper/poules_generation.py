# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view permettant de générer une poule pour un tournoi
'''
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Court, Poule, PouleStatus, LogActivity, Tournoi, TournoiStatus, infoTournoi, TournoiTitle, TournoiCategorie
from tennis.views import staffTournoi
from datetime import date
from tennis.views import generatePool, home
from tennis.mail import send_email_start_tournament
from math import ceil

def view(request, name):
    title = name
    cat = name
    if "_" in name:
        title = name.split("_")[0]
        cat = name.split("_")[1]
    ti = TournoiTitle.objects.get(nom=title)
    ca = TournoiCategorie.objects.get(nom=cat)
    tournoi = Tournoi.objects.get(titre=ti, categorie=ca)
    terrains = Court.objects.filter(valide=True)
    allPair = Pair.objects.filter(tournoi=tournoi, valid=True)
    for my_pair in allPair:
        my_pair.smallName1 = my_pair.user1.participant.small_name_classement()
        my_pair.smallName2 = my_pair.user2.participant.small_name_classement()
    poules = Poule.objects.filter(tournoi=tournoi)

    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    infTournoi = info
    infLng = infTournoi.longitude
    infLat = infTournoi.latitude

    jour = tournoi.titre.jour
    if jour == "Samedi":
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
            LogActivity(user=request.user, section="Tournoi", target=""+tournoi.nom(),
                        details=u"Génération des poules du tournoi : " + tournoi.nom()).save()

        i = 0
        j = -1
        pouleDict = {}
        while i < len(pairspoulesList):
            if pairspoulesList[i].startswith('[') and pairspoulesList[i].endswith(']'):
                j += 1
                pouleDict[j] = {}
                pouleDict[j]['pairList'] = []
                if terrainsList[j] != '':
                    pouleDict[j]['terrain'] = Court.objects.get(
                        id=terrainsList[j])
                pouleDict[j]['leaderName'] = leadersList[j]
            else:
                pair = Pair.objects.get(id=pairspoulesList[i])
                pouleDict[j]['pairList'].append(pair)
                user1fullname = pair.user1.participant.prenom + ' ' + pair.user1.participant.nom
                user2fullname = pair.user2.participant.prenom + ' ' + pair.user2.participant.nom
                if user1fullname == pouleDict[j]['leaderName']:
                    pouleDict[j]['leader'] = pair.user1
                elif user2fullname == pouleDict[j]['leaderName']:
                    pouleDict[j]['leader'] = pair.user2

            i += 1
        i = 0

        # Au lieu de delete on parcours la liste
        # Poule.objects.filter(tournoi=tournoi).delete()
        score_list = list()
        # On parcours et on garde les scores
        for elem in Poule.objects.filter(tournoi=tournoi):
            p2 = Poule(tournoi=tournoi)
            p2.status = elem.status
            p2.save()
            for p in elem.paires.all():
                p.smallName1 = p.user1.participant.small_name_classement()
                p.smallName2 = p.user2.participant.small_name_classement()
                p2.paires.add(p)
            for p in elem.score.all():
                p2.score.add(p)
            score_list.append(p2)
            elem.delete()

        finali = True
        while i <= j:
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
            # check si c'est les meme pair qu'une des liste
            for elem in score_list:
                pair_list = sorted(elem.paires.all(), key=lambda x: x.id)
                pair_list2 = sorted(p.paires.all(), key=lambda x: x.id)
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

        if finali:
            tournoi.status = TournoiStatus.objects.get(numero=3)
            tournoi.save()
        else:
            tournoi.status = TournoiStatus.objects.get(numero=2)
            tournoi.save()

        if request.POST['action'] == 'save':
            tournoi.status = TournoiStatus.objects.get(numero=1)
            tournoi.save()
            return redirect(reverse(generatePool, args={tournoi.nom()}))
            #request.method = "GET"
            # return generatePool(request,tournoi.nom)
            # return
            # HttpResponseRedirect('/staff/tournois/%s'%tournoi.nom)
        else:
	    # TODO
	    send_email_start_tournament(request.user, tournoi)
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
            defaultValue = int(ceil((len(allPair) / defaultSize)))
            poolRange = range(0, defaultValue)
            pairListAll = dict()
            for x in range(0, defaultValue):
                index = int(x * defaultSize)
                pairListAll[x + 1] = (allPair[index:index + int(defaultSize)])
                if x == defaultValue - 1:
                    v = int(defaultSize) - len(pairListAll[x + 1])
            today = date.today()
            for elem in allPair:
                u1 = elem.user1
                born = u1.participant.datenaissance
                u1.age = today.year - born.year - \
                    ((today.month, today.day) < (born.month, born.day))
                u2 = elem.user2
                born = u2.participant.datenaissance
                u2.age = today.year - born.year - \
                    ((today.month, today.day) < (born.month, born.day))
                c1 = ""
                c2 = ""
                if elem.comment1:
                    c1 = str(elem.comment1)
                if elem.comment2:
                    c2 = str(elem.comment2)
                if c1 != "" or c2 != "":
                    elem.commentaires = c1 + "<hr>" + c2
            return render(request, 'generatePool.html', locals())
        else:
            saved = True

            defaultValue = len(listPoules)
            defaultSize = 0
            pairListAll = dict()
            today = date.today()
            i = 0
            for poule in listPoules:
                pairListAll[i + 1] = []
                listTerrainSaved.append(poule.court)
                listLeaderSaved.append(poule.leader)
                if defaultSize < len(poule.paires.all()):
                    defaultSize = len(poule.paires.all())
                for elem in poule.paires.all():
                    u1 = elem.user1
                    born = u1.participant.datenaissance
                    u1.age = today.year - born.year - \
                        ((today.month, today.day) < (born.month, born.day))
                    u2 = elem.user2
                    born = u2.participant.datenaissance
                    u2.age = today.year - born.year - \
                        ((today.month, today.day) < (born.month, born.day))
                    c1 = ""
                    c2 = ""
                    elem.smallName1 = elem.user1.participant.small_name_classement()
                    elem.smallName2 = elem.user2.participant.small_name_classement()
                    if elem.comment1:
                        c1 = str(elem.comment1)
                    if elem.comment2:
                        c2 = str(elem.comment2)
                    if c1 != "" or c2 != "":
                        elem.commentaires = c1 + "<hr>" + c2
                    pairListAll[i + 1].append(elem)
                i += 1
            poolRange = range(0, defaultValue)
            return render(request, 'generatePool.html', locals())
    return redirect(reverse(home))
