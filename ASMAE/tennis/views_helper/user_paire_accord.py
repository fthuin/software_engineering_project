# /usr/bin/env python
# coding: utf8

'''
Implémentation de la view affichant à un utilisateur qui a été demandé en
tant que deuxième joueur la possibilité d'accepter ou de refuser la paire
proposée
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
    if pair.user2 != request.user:
        return redirect(reverse(tournoi))
    if request.method == "POST":
        if request.POST['action'] == "validate":
            remarque = request.POST['remarque']
            extra = request.POST.getlist('extra')

            pair.confirm = True
            pair.comment2 = remarque
            pair.save()

            for elem in extra:
                ext = Extra.objects.get(id=elem)
                pair.extra2.add(ext)

            pair.save()

            return redirect(reverse(tournoi))
        if request.POST['action'] == "refuse":

            pair.delete()
            return redirect(reverse(tournoi))
            # TODO Envoyer mail a l'user 1 pour lui dire que son pote veut pas
            # de lui
    if request.user.is_authenticated():
        # TODO check si il peut confirmer cette pair

        extra1 = pair.extra1.all()
        extranot1 = list()
        Ex = Extra.objects.all()
        for elem in Ex:
            contained = False
            for el in extra1:
                if elem.id == el.id:
                    contained = True
            if contained == False:
                extranot1.append(Extra.objects.get(id=elem.id))

        return render(request, 'confirmPair.html', locals())
    return redirect(reverse(home))
