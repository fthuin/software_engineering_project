# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui affiche un résumé de toutes les poules créées
avec la possibilité d'aller vers la page de score ou de supprimer les poules
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Tournoi, TournoiTitle, TournoiStatus, TournoiCategorie, Poule, PouleStatus, LogActivity
from tennis.views import home, generatePool


def view(request, name):
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
                    details="Suppression des poules du tournoi : " + tournoi.nom()).save()
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
