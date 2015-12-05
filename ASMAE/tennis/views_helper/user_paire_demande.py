# /usr/bin/env python
# coding: utf8

'''
Implémentation de la view permettant à un utilisateur de voir une paire
en attente de confirmation de la part de l'autre joueur
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Extra
from tennis.views import home, tournoi

def view(request, id):
    pair = Pair.objects.filter(id=id)
    if len(pair) < 1:
        return redirect(reverse(tournoi))
    pair = Pair.objects.get(id=id)
    if pair.user1 != request.user:
        return redirect(reverse(tournoi))
    if request.method == "POST":
        # TODO check si il peut annuler cette pair
        pair.delete()
        return redirect(reverse(tournoi))
    if request.user.is_authenticated():

        extra1 = pair.extra1.all()
        Ex = Extra.objects.all()
        extranot1 = list()
        for elem in Ex:
            contained = False
            for el in extra1:
                if elem.id == el.id:
                    contained = True
            if contained == False:
                extranot1.append(Extra.objects.get(id=elem.id))

        return render(request, 'cancelPair.html', locals())
    return redirect(reverse(home))
