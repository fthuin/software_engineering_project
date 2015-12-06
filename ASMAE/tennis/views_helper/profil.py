# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view de consultation ou de modification du profil
'''
from tennis.models import Participant, UserInWaitOfActivation, Ranking
import datetime
from tennis.mail import send_register_confirmation_email
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import re
from tennis.classement import validate_classement_thread
from django.core.urlresolvers import reverse
from tennis.views import home
from django.core.exceptions import ObjectDoesNotExist

def view(request):
    rankings = Ranking.objects.all()
    today = datetime.date.today()
    yearLoop = range(1900, today.year - 7)
    try:
        request.user.participant
    except ObjectDoesNotExist:
        Participant(user=request.user, titre = "Mr", nom="", prenom="", rue="",
        numero="", boite="", codepostal="", localite="", telephone="", fax="",
        gsm="", classement=rankings.first(), oldparticipant=False,
        datenaissance=today, latitude=0.0, isClassementVerified=False,
         longitude=0.0).save()
    birthdate = request.user.participant.datenaissance
    formatedBirthdate = birthdate.strftime('%d/%m/%Y')
    if request.method == "POST":
        if request.POST['action'] == 'sendMailConfirmationMail':
            # Send email with code to finish registration and validate account
            participant = Participant.objects.get(user=request.user)
            activationObject = UserInWaitOfActivation.objects.get(
                participant=participant)
            activationObject.dayOfRegistration = datetime.datetime.now()
            activationObject.save()
            link = "http://" + request.get_host() + "/tennis/emailValidation/"
            if send_register_confirmation_email(activationObject, participant, link):
                successSendMail = u"Un email vous a été renvoyé sur votre adresse courante. En cas de non-réception, veuillez revérifier l'adresse enregistrée ci-dessous."
            else:
                echecSendMail = u"Une erreur s'est produite lors de l'envois de votre message,\nle problème a été signaler au staff et sera résolu dans les plus bref délais.\nDésole de l'inconvénience, réessayer dans quelques heures"
            return render(request, 'profil.html', locals())
        if request.POST['action'] == 'updatePassword':

            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # On vérifie que les password sont les memes
            if password1 != password2:
                errorMDP = "Les mots de passes sont différents !"
                return render(request, 'profil.html', locals())

            # On vérifie la longeur du password
            if(len(password1) < 2):
                errorMDP = "Votre mot de passe doit contenir au moins 3 caractères"
                return render(request, 'profil.html', locals())

            request.user.set_password(password1)
            request.user.save()
            successMDP = "Le mot de passe a bien été changé"
            user2 = authenticate(username=request.user, password=password1)
            login(request, user2)
            return render(request, 'profil.html', locals())

        if request.POST['action'] == 'editProfil':

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

            if request.POST.__contains__("participated"):
                oldparticipant = True
            else:
                oldparticipant = False

            # check champs
            if (firstname == "" or lastname == "" or (tel == ""
                                                      and gsm == "") or street == "" or number == "" or locality == "" or postalcode == "" or birthdate == ""):
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

            formatedBirthdate = birthdate
            participant = request.user.participant
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
            participant.oldparticipant = oldparticipant
            participant.latitude = lat
            participant.longitude = lng
            participant.save()

            # Validate classement
            validate_classement_thread(participant)

            successEdit = "Le profil a bien été changé"
            return render(request, 'profil.html', locals())

    if request.user.is_authenticated():

        return render(request, 'profil.html', locals())
    return redirect(reverse(home))
