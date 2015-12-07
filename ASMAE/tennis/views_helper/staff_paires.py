# /usr/bin/env python
# coding: utf8

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Pair, Tournoi, TournoiCategorie, TournoiTitle
from django.db.models import Q
from tennis.views import home, db_type

def view(request):
    page = 1
    pageLength = 10
    recherche = ""
    validation = ""
    paiement = ""
    tournoi = ""
    if request.method == 'POST':
        page = request.POST['page']
        pageLength = int(request.POST['pagelength'])
        recherche = request.POST['rechercheField'].strip()
        validation = request.POST['validation']
        paiement = request.POST['paiement']
        tournoi = request.POST['tournoi']

    allPair = Pair.objects.all()

    if recherche != "":
        allPair = allPair.filter(
            Q(id__icontains=recherche) |
            Q(user1__username__icontains=recherche) |
            Q(user1__participant__nom__icontains=recherche) |
            Q(user1__participant__prenom__icontains=recherche) |
            Q(user2__username__icontains=recherche) |
            Q(user2__participant__nom__icontains=recherche) |
            Q(user2__participant__prenom__icontains=recherche))

    if validation != "":
        if validation == "True":
            allPair = allPair.filter(valid=True)
        else:
            allPair = allPair.filter(valid=False)

    if paiement != "":
        if paiement == "True":
            allPair = allPair.filter(pay=True)
        else:
            allPair = allPair.filter(pay=False)

    if tournoi != "":
        title = tournoi
        cat = tournoi
        if "_" in tournoi:
            title = tournoi.split("_")[0]
            cat = tournoi.split("_")[1]
        t = TournoiTitle.objects.get(nom=title)
        c = TournoiCategorie.objects.get(nom=cat)
        new_tournoi = Tournoi.objects.get(titre=t, categorie=c)
        allPair = allPair.filter(tournoi=new_tournoi)

    allPair = allPair.order_by("id")
    length = len(allPair)
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    allPair = allPair[debut - 1:fin]
    Tour = Tournoi.objects.all()

    if request.user.is_authenticated():
        return render(request, 'staffPair.html', locals())
    return redirect(reverse(home))
