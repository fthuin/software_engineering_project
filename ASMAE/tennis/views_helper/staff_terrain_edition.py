# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view contenant un formulaire de modification des
informations relatives à un terrain.
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Court, CourtType, CourtSurface, CourtState, LogActivity
from tennis.views import validateTerrain, staffTerrain, home

def view(request, id):
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
            matiere = (u'' + request.POST['matiere']).encode('utf-8')
            type = request.POST['type']
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
            court.longitude = lng
            court.latitude = lat
            court.save()
            LogActivity(user=request.user, section="Terrain", target=""+id,
                        details=u"Terrain édité").save()
            #successEdit = "Terrain "+str(id)+" bien édité!"
            return redirect(reverse(validateTerrain, args={id}))

        if request.POST['action'] == "deleteCourt":
            court.delete()
            LogActivity(user=request.user, section="Terrain", target=""+id,
                        details=u"Terrain supprimé").save()
            return redirect(reverse(staffTerrain))
    if request.user.is_authenticated():
        return render(request, 'editTerrainStaff.html', locals())
    return redirect(reverse(home))
