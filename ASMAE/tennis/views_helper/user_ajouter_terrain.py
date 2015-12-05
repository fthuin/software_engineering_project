# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view permettant à un utilisateur de rajouter un terrain.
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Participant, Court, CourtSurface, CourtType, CourtState
from tennis.mail import send_confirmation_email_court_registered
from tennis.views import home, terrain


def view(request):
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

        if rue == "" or numero == "" or postalcode == "" or locality == "" or matiere == "" or type == "" or etat == "":
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
