# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view de création d'un compte
'''
import datetime
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Participant, Ranking, UserInWaitOfActivation
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
from tennis.classement import validate_classement_thread
from tennis.mail import register_confirmation_email
from tennis.views import tournoi

def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


def email_present(email):
    if User.objects.filter(email=email).exists():
        return True
    return False

def view(request):
    today = datetime.date.today()
    yearLoop = range(1900, today.year - 7)
    rankings = Ranking.objects.all()
    if request.method == "POST":
        # Recuperation des donnees
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
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
        if (username == "" or password == "" or firstname == "" or lastname == "" or email == "" or (tel == ""
                                                                                                     and gsm == "") or street == "" or number == "" or locality == "" or postalcode == "" or birthdate == ""):
            error = "Veuillez remplir tous les champs obligatoires !"
            return render(request, 'register.html', locals())

        # Check username et email already taken
        if username_present(username):
            error = "Ce nom d'utilisateur n'est plus disponible !"
            return render(request, 'register.html', locals())

        # On vérifie si l'email est deja dans la db
        if(email_present(email)):
            error = "Un compte avec cette addresse email existe déjà !"
            return render(request, 'register.html', locals())

        # check username length
        if len(username) < 2:
            error = "Votre nom d'utilisateur doit contenir au moins 3 caractères"
            return render(request, 'register.html', locals())

        # check password length
        if len(password) < 2:
            error = "Votre mot de passe doit contenir au moins 3 caractères"
            return render(request, 'register.html', locals())

        # check format date
        if re.match(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$", birthdate) is None:
            error = "La date de naissance n'a pas le bon format"
            return render(request, 'register.html', locals())

        # On format la date
        birthdate2 = birthdate.split("/")
        datenaissance = datetime.datetime(
            int(birthdate2[2]), int(birthdate2[1]), int(birthdate2[0]))

        # Account creation & redirect
        user = User.objects.create_user(username, email, password)
        user.save()
        # TODO verfied = FALSE
        participant = Participant(user=user, titre=title, nom=lastname, prenom=firstname, rue=street, numero=number, boite=boite, codepostal=postalcode, localite=locality, telephone=tel, fax=fax, gsm=gsm,
                                  classement=Ranking.objects.get(nom=classement), oldparticipant=oldparticipant, datenaissance=datenaissance, isClassementVerified=True, isAccountActivated=False, latitude=lat, longitude=lng)
        participant.save()

        # Create UserInWaitOfActivation object to keep track of the activation
        today = datetime.datetime.now()
        key = get_random_string(
            20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        while len(UserInWaitOfActivation.objects.filter(confirmation_key=key)) > 0:
            # Key already in user, generate new one
            key = get_random_string(
                20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        activationObject = UserInWaitOfActivation(
            participant=participant, dayOfRegistration=today, confirmation_key=key)
        activationObject.save()
        link = "http://" + request.get_host() + "/tennis/emailValidation/"

        # Verify user classement
        validate_classement_thread(participant)

        # Send email with code to finish registration and validate account
        register_confirmation_email(activationObject, participant, link)

        # On connecte l'utilisateur
        user2 = authenticate(username=username, password=password)
        login(request, user2)
        return redirect(reverse(tournoi))

    if request.user.is_authenticated():
        return redirect(reverse(tournoi))
    return render(request, 'register.html', locals())
