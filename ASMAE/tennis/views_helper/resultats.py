# /usr/bin/env python
# coding: utf8
'''
Implémentation de la page qui affiche les résultats des tournois pour chaque
année
'''

from tennis.models import TournoiTitle, infoTournoi
from django.shortcuts import render

def view(request, id):
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
