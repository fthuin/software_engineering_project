# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet à un utilisateur de voir une paire
qui a été formée (acceptée par le deuxième joueur)
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Extra
from tennis.views import home, tournoi

def view(request, id):
    if request.method == "POST":
        pair = Pair.objects.filter(id=id)
        pair.delete()
        return redirect(reverse(tournoi))
    pair = Pair.objects.filter(id=id)
    if len(pair) < 1:
        return redirect(reverse(tournoi))
    pair = Pair.objects.get(id=id)
    if pair.user1 != request.user and pair.user2 != request.user:
        return redirect(reverse(tournoi))
    if request.user.is_authenticated():
        Ex = Extra.objects.all()
        extra1 = pair.extra1.all()
        extranot1 = list()
        for elem in Ex:
            contained = False
            for el in extra1:
                if elem.id == el.id:
                    contained = True
            if contained == False:
                extranot1.append(Extra.objects.get(id=elem.id))

        extra2 = pair.extra2.all()
        extranot2 = list()
        for elem in Ex:
            contained = False
            for el in extra2:
                if elem.id == el.id:
                    contained = True
            if contained == False:
                extranot2.append(Extra.objects.get(id=elem.id))
        return render(request, 'viewPair.html', locals())
    return redirect(reverse(home))
