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
        #if request.POST['action'] == "search":
        page = request.POST['page']
        pageLength = int(request.POST['pagelength'])
        recherche = request.POST['rechercheField'].strip()
        validation = request.POST['validation']
        paiement = request.POST['paiement']
        tournoi = request.POST['tournoi']
        if request.POST['action'] == "CSV":
            #TODO florian
            pass

    allPair = Pair.objects.filter(confirm=True)

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

    if request.method == 'POST':
        if request.POST['action'] == "CSV":
            import csv
            from django.utils.encoding import smart_str
            from django.http import HttpResponse
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Participants.csv'
            writer = csv.writer(response, csv.excel)
            # BOM (optional...Excel needs it to open UTF-8 file properly)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"ID"),
                smart_str(u"Tournoi"),
                smart_str(u"Catégorie"),
                smart_str(u"Joueur 1"),
                smart_str(u"Joueur 2"),
                smart_str(u"Validation"),
                smart_str(u"Paiement"),
                smart_str(u"Extra joueur 1"),
                smart_str(u"Extra joueur 2")
            ])
            for obj in allPair:
                extra_joueur_1 = ""
                for ex_joueur1 in obj.extra1.all():
                    extra_joueur_1 += ex_joueur1.nom + " "
                extra_joueur_2 = ""
                for ex_joueur2 in obj.extra2.all():
                    extra_joueur_2 += ex_joueur2.nom + " "
                writer.writerow([
                    smart_str(obj.id),
                    smart_str(obj.tournoi.titre.nom),
                    smart_str(obj.tournoi.categorie.nom),
                    smart_str(obj.user1.participant.codeName()),
                    smart_str(obj.user2.participant.codeName()),
                    smart_str(obj.valid),
                    smart_str(obj.pay),
                    smart_str(extra_joueur_1.strip()),
                    smart_str(extra_joueur_2.strip())
                ])
            return response

    if request.user.is_authenticated():
        return render(request, 'staffPair.html', locals())
    return redirect(reverse(home))
