# /usr/bin/env python
# coding: utf8
'''
Implémentation de la vue permettant de créer l'arbre pour les matches de
l'après-midi
'''
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Poule, PouleStatus, Court, Tournoi, TournoiTitle, TournoiCategorie, TournoiStatus, LogActivity, Arbre, infoTournoi, Resultat
from tennis.views import home, knockOff

def view(request, name):
    title = name
    cat = name
    if "_" in name:
        title = name.split("_")[0]
        cat = name.split("_")[1]
    ti = TournoiTitle.objects.get(nom=title)
    ca = TournoiCategorie.objects.get(nom=cat)
    tournoi = Tournoi.objects.get(titre=ti, categorie=ca)
    # Liste des tournoi qui ont deja un arbre
    all_tournoi_with_arbre = Tournoi.objects.filter(
        arbre__id__gte=0).exclude(titre=ti, categorie=ca)
    court_list = dict()

    for elem in all_tournoi_with_arbre:
        if elem.arbre.court.id in court_list:
            court_list[elem.arbre.court.id] += "<br>" + str(elem)
        else:
            court_list[elem.arbre.court.id] = str(elem)

    all_tournoi_with_arbre = None

    terrains = Court.objects.filter(valide=True)

    jour = ti.jour
    if jour == "Samedi":
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
            pair_g = None
            if gagnant != "":
                pairgagnante = Pair.objects.get(id=int(gagnant))
                pairgagnante.gagnant = True
                pairgagnante.save()
                pair_g = pairgagnante

            pair_f = None
            if finaliste != "":
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
                # Changement du status du tournoi
                s = TournoiStatus.objects.get(numero=4)
                tournoi.status = s
                tournoi.save()

                # Save des resultats
                for elem in Resultat.objects.filter(tournoi=tournoi):
                    elem.delete()
                ga = pair_g.user1.participant.prenom + u" " + pair_g.user1.participant.nom.upper() + \
                    u" et " + pair_g.user2.participant.prenom + \
                    u" " + pair_g.user2.participant.nom.upper()
                fi = pair_f.user1.participant.prenom + u" " + pair_f.user1.participant.nom.upper() + \
                    u" et " + pair_f.user2.participant.prenom + \
                    u" " + pair_f.user2.participant.nom.upper()
                r = Resultat(tournoi=tournoi, gagnants_alt=ga,
                             finalistes_alt=fi)
                r.save()
                r.gagnants.add(pair_g.user1)
                r.gagnants.add(pair_g.user2)
                r.finalistes.add(pair_f.user1)
                r.finalistes.add(pair_f.user2)
                r.save()
                info = infoTournoi.objects.all()
                info = info.order_by("edition")[len(info) - 1]
                info.resultats.add(r)
                info.save()

            if tournoi.arbre is None:
                arbre = Arbre(data=treeData, label=treeLabel)
                arbre.court = terrain
                arbre.save()
                tournoi.arbre = arbre
                tournoi.save()
            else:
                arbre = tournoi.arbre
                arbre.data = treeData
                arbre.label = treeLabel
                arbre.court = terrain
                arbre.save()
                LogActivity(user=request.user, section="Tournoi",
                            details="Mise a jour de l'abre du tournoi : " + tournoi.nom()).save()

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
                LogActivity(user=request.user, section="Tournoi",
                            details="Suppression de l'abre du tournoi : " + tournoi.nom()).save()
                return redirect(reverse(knockOff, args={name}))

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
                x = 1
                for pairID, sc in liste:
                    pai = Pair.objects.get(id=pairID)
                    pai.score = sc
                    pai.poule = poule.id
                    pai.position = x
                    poule.SortedPair.append(pai)
                    allPaires.append(pai)
                    x = x + 1
        if tournoi.arbre is not None:
            arbre = tournoi.arbre
        return render(request, 'knockOff.html', locals())
    return redirect(reverse(home))
