# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet à un utilisateur de modifier un terrain
qu'il a précédemment enregistré
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Court, CourtSurface, CourtType, CourtState
from tennis.views import home, terrain

def view(request, id):
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

            if rue == "" or numero == "" or postalcode == "" or locality == "" or matiere == "" or type == "" or etat == "":
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
