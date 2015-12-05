# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view permettant au staff de voir tous les terrains
enregistrés sur le système.
'''

from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Court, CourtSurface, CourtType, CourtState
from tennis.views import home, db_type

def view(request):
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
