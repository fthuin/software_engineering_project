# /usr/bin/env python
# coding: utf8

'''
Implémentation de la view permettant à deux joueurs d'une paire de payer.
Contient un récapitulatif des tarifs et un mode de paiement.
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Extra, infoTournoi
from tennis.views import home, tournoi

def view(request, id):
    pair = Pair.objects.filter(id=id)
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    prix = info.prix
    if len(pair) < 1:
        return redirect(reverse(tournoi))
    pair = Pair.objects.get(id=id)
    if pair.user1 != request.user and pair.user2 != request.user:
        return redirect(reverse(tournoi))
    if request.user.is_authenticated():
        # TODO check si il peut payer cette pair
        allExtras = Extra.objects.all()
        extra1 = pair.extra1.all()
        extra2 = pair.extra2.all()
        totalprice = 2 * float(prix)
        listUniqueExtra = list(set(list(extra1) + list(extra2)))
        extraList = []
        for extra in listUniqueExtra:
            count = 0
            for e1 in extra1:
                if extra.id == e1.id:
                    count += 1
            for e2 in extra2:
                if extra.id == e2.id:
                    count += 1
            extraList.append((extra.nom, extra.prix, count))
            totalprice += float(count * extra.prix)

        return render(request, 'payPair.html', locals())
    return redirect(reverse(home))
