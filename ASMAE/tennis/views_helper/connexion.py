# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view de connexion d'un utilisateur au site
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from tennis.views import tournoi

def view(request):
    if request.method == "POST":
        # Recuperation des donnees
        username = request.POST['username']
        password = request.POST['password']

        # check email
        if username == "":
            error = "Veuillez entrer un nom d'utilisateur valide !"
            return render(request, 'login.html', locals())

        # check password
        if password == "":
            error = "Veuillez entrer un mot de passe !"
            return render(request, 'login.html', locals())

        # Connection
        user = authenticate(username=username, password=password)
        # Si l'utilisateur existe et qu'il est actif on le connecte sinon on
        # affiche un message d'erreur
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse(tournoi))
            else:
                error = "Ce compte a été désactivé !"
                return render(request, 'login.html', locals())
        else:
            # invalide login
            error = "Nom d'utilisateur ou mot de passe incorrect !"
            return render(request, 'login.html', locals())
    return render(request, 'login.html', locals())
