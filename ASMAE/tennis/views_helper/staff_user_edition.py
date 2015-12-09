# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet à un membre du staff de voir les
informations sur une personne et de les modifier
'''

from itertools import chain
import datetime
from tennis.models import Court, Pair, Ranking, LogActivity
from django.contrib.auth.models import User
import re
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.classement import validate_classement_thread
from tennis.views import home

def view(request, name):
    rankings = Ranking.objects.all()

    use = User.objects.get(username=name)
    today = datetime.date.today()
    yearLoop = range(1900, today.year - 7)
    birthdate = use.participant.datenaissance
    formatedBirthdate = birthdate.strftime('%d/%m/%Y')
    terrain = Court.objects.filter(user=use)
    tournoi1 = Pair.objects.filter(user1=use, confirm=True)
    tournoi2 = Pair.objects.filter(user2=use, confirm=True)
    tournoi = list(chain(tournoi1, tournoi2))

    user_logs = LogActivity.objects.filter(section="Utilisateur", target=use.username).order_by('-date')[:10]

    if request.method == "POST":
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gsm = request.POST['gsm']
        tel = request.POST['tel']
        fax = request.POST['fax']
        title = request.POST['title']
        boite = request.POST['boite']
        street = request.POST['street']
        number = request.POST['number']
        locality = request.POST['locality']
        postalcode = request.POST['postalcode']
        birthdate = request.POST['birthdate']
        classement = request.POST['classement']
        lat = request.POST['lat']
        lng = request.POST['lng']

        # check champs
        if firstname == "" or lastname == "" or (tel == "" and gsm == "") or street == "" or number == "" or locality == "" or postalcode == "" or birthdate == "":
            errorEdit = "Veuillez remplir tous les champs obligatoires !"
            return render(request, 'profil.html', locals())

        # check format date
        if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$", birthdate) is None:
            errorEdit = "La date de naissance n'a pas le bon format"
            return render(request, 'profil.html', locals())

        # On formate la date
        birthdate2 = birthdate.split("/")
        datenaissance = datetime.datetime(
            int(birthdate2[2]), int(birthdate2[1]), int(birthdate2[0]))

        use.email = email
        use.save()

        formatedBirthdate = birthdate
        participant = use.participant
        participant.titre = title
        participant.nom = lastname
        participant.prenom = firstname
        participant.rue = street
        participant.numero = number
        participant.boite = boite
        participant.codepostal = postalcode
        participant.localite = locality
        participant.telephone = tel
        participant.fax = fax
        participant.gsm = gsm
        participant.datenaissance = datenaissance
        participant.classement = Ranking.objects.get(nom=classement)
        participant.latitude = lat
        participant.longitude = lng
        participant.save()

        # Validate classement
        validate_classement_thread(participant)
        LogActivity(user=request.user, section="Utilisateur",
                target=""+use.username, details=u"Profil de " + use.username + u" modifié").save()
        successEdit = "Le profil a bien été changé"

    use = User.objects.get(username=name)
    today = datetime.date.today()
    yearLoop = range(1900, today.year - 7)
    birthdate = use.participant.datenaissance
    formatedBirthdate = birthdate.strftime('%d/%m/%Y')
    terrain = Court.objects.filter(user=use)
    tournoi1 = Pair.objects.filter(user1=use, confirm=True)
    tournoi2 = Pair.objects.filter(user2=use, confirm=True)
    tournoi = list(chain(tournoi1, tournoi2))

    if request.user.is_authenticated():
        return render(request, 'viewUser.html', locals())
    return redirect(reverse(home))
