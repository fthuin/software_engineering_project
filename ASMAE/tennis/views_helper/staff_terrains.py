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
from tennis.views import home
from django.http import HttpResponse

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
        #if request.POST['action'] == "search":
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

    print(repr(len(allCourt)))

    if request.method == 'POST':
        if request.POST['action'] == "CSV":
            import csv
            from django.utils.encoding import smart_str
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Terrains.csv'
            writer = csv.writer(response, csv.excel)
            # BOM (optional...Excel needs it to open UTF-8 file properly)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"ID"),
                smart_str(u"Rue"),
                smart_str(u"Numéro"),
                smart_str(u"Boîte"),
                smart_str(u"Code postal"),
                smart_str(u"Localité"),
                smart_str(u"Latitude"),
                smart_str(u"Longitude"),
                smart_str(u"Accès"),
                smart_str(u"Surface"),
                smart_str(u"Type"),
                smart_str(u"Samedi"),
                smart_str(u"Dimanche"),
                smart_str(u"Etat"),
                smart_str(u"Comm. propriétaire"),
                smart_str(u"Comm. staff"),
                smart_str(u"Validé"),
                smart_str(u"Username"),
                smart_str(u"email"),
                smart_str(u"Prénom du propriétaire"),
                smart_str(u"Nom du propriétaire"),
                smart_str(u"Utilisé l'année passée"),
            ])
            for obj in allCourt:
                writer.writerow([
                    smart_str(obj.id),
                    smart_str(obj.rue),
                    smart_str(obj.numero),
                    smart_str(obj.boite),
                    smart_str(obj.codepostal),
                    smart_str(obj.localite),
                    smart_str(obj.latitude),
                    smart_str(obj.longitude),
                    smart_str(obj.acces),
                    smart_str(obj.matiere.nom),
                    smart_str(obj.type.nom),
                    smart_str(obj.dispoSamedi),
                    smart_str(obj.dispoDimanche),
                    smart_str(obj.etat.nom),
                    smart_str(obj.commentaire),
                    smart_str(obj.commentaireStaff),
                    smart_str(obj.valide),
                    smart_str(obj.user.username),
                    smart_str(obj.user.email),
                    smart_str(obj.user.participant.prenom),
                    smart_str(obj.user.participant.nom),
                    smart_str(obj.usedLastYear),
                ])
            return response

    if request.user.is_authenticated():
        return render(request, 'staffTerrain.html', locals())
    return redirect(reverse(home))
