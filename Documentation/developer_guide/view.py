def sponsors(request):
    return render(request, 'sponsors.html', {})

# coding=utf-8
'''
This file contains all the urls available and their links
to a view in views.py
'''
from django.conf.urls import url, patterns

urlpatterns = patterns('tennis.views',
                       url(r'^$', 'home'),
                       url(r'^connexion$', 'connect'),
                       url(r'^deconnexion$', 'deconnect'),
                       url(r'^inscription$', 'register'),
                       url(r'^sponsors$', 'sponsors'),
                       url(r'^contact$', 'contact'),
                       )

def terrain(request):
    if request.user.is_authenticated():
        court = Court.objects.filter(user=request.user)
        return render(request, 'terrain.html', locals())
    return redirect(reverse(home))

def view(request):
    if request.method == "POST":
        # Recuperation des donnees
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Account creation & redirect
        user = User.objects.create_user(username, email, password)
        user.save()

        # On connecte l'utilisateur
        user2 = authenticate(username=username, password=password)
        login(request, user2)
        return redirect(reverse(tournoi))