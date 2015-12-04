# coding: utf8
from tennis.models import Participant, infoTournoi
from itertools import chain
from datetime import timedelta
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.views import home

def view(request):
    if request.user.is_authenticated():
        if Participant.objects.get(user=request.user).isAccountActivated:
            nonComfirme = request.user.user1.filter(confirm=False)
            demande = request.user.user2.filter(confirm=False)
            inscrit1 = request.user.user1.filter(confirm=True)
            inscrit2 = request.user.user2.filter(confirm=True)
            inscrit = list(chain(inscrit1, inscrit2))
            agenda = False
            info = infoTournoi.objects.all()
            info = info.order_by("edition")[len(info) - 1]
            date1 = info.date
            date2 = date1 + timedelta(days=1)
            for elem in inscrit:
                if elem.tournoi.titre.jour == "Samedi":
                    elem.date = date1.strftime('%d/%m/%Y')
                else:
                    elem.date = date2.strftime('%d/%m/%Y')
                if elem.valid and elem.tournoi.status.numero >= 2:
                    agenda = True
            return render(request, 'tournoi.html', locals())
        else:
            return render(request, 'tournoiUserNotValidated.html', locals())
    return redirect(reverse(home))
