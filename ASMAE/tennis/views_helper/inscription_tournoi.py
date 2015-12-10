# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view permettant l'inscription d'un utilisateur à un tournoi
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tennis.models import Pair, Tournoi, Extra, infoTournoi, Participant, TournoiTitle, TournoiCategorie
from django.db.models import Q
from tennis.views import yearsago, tournoi, home
from tennis.mail import send_confirmation_email_pair_registered
from operator import or_

def view(request):
    page = 1
    pageLength = 10
    recherche = ""
    if request.method == 'POST':
        if request.POST['action'] == "search":
            page = request.POST['page']
            recherche = request.POST['rechercheField'].strip()

    Ex = Extra.objects.only
    Tour = Tournoi.objects.all()
    # Liste des user ordered et sans sois meme
    Use = User.objects.all().order_by('username').exclude(
        username=request.user.username)
    # On retire les staff et les admins
    Use = Use.exclude(is_staff=True).exclude(
        groups__name="Admin").exclude(groups__name="staff")

    if recherche != "":
        Use = Use.filter(
            Q(username__icontains=recherche) |
            Q(participant__nom__icontains=recherche) |
            Q(participant__prenom__icontains=recherche))

    # Utilisateur courant
    u = request.user

    # Recuperations des infos
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    today = info.date

    # Tri de la liste

    # Libre samedi/dimanche
    libre_Samedi = True
    libre_Dimanche = True
    for elem in u.user1.all() or u.user2.all():
        if elem.tournoi.titre.jour == "Samedi":
            libre_Samedi = False
        else:
            libre_Dimanche = False

    famille_25 = yearsago(25, today.replace(month=1,day=1))
    famille_15 = yearsago(15, today.replace(month=1,day=1))

    querysets = list()
    # Liste contenant les utilisateurs pour le tournoi des familles
    famille_list = list()
    if libre_Samedi:
        # Check tournoi des familles
        #- de 15 ans
        if u.participant.datenaissance >= famille_15:
            # On garde les utilisateur de + de 25 ans
            famille_list = Use.filter(
                participant__datenaissance__lte=famille_25)
            # On retire ceux qui ne sont pas libre le samedi
            famille_list = famille_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(
                user2__tournoi__titre__jour="Samedi")
            querysets.append(famille_list)
        #+ de 25 ans
        elif u.participant.datenaissance <= famille_25:
            # On garde les utilisateur de - de 15 ans
            famille_list = Use.filter(
                participant__datenaissance__gte=famille_15)
            # On retire ceux qui ne sont pas libre le samedi
            famille_list = famille_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(
                user2__tournoi__titre__jour="Samedi")
            querysets.append(famille_list)

    # Liste du samedi (except tournoi des familles)
    samedi_list = list()
    if libre_Samedi:
        # On prend seulement les joueur du sexe opposé
        samedi_list = Use.exclude(participant__titre=u.participant.titre)
        # On retire ceux qui ne sont pas libre samedi
        samedi_list = samedi_list.exclude(user1__tournoi__titre__jour="Samedi").exclude(
            user2__tournoi__titre__jour="Samedi")
        querysets.append(samedi_list)

    # Liste du dimanche
    dimanche_list = list()
    if libre_Dimanche:
        # On prend seulement les joueurs du meme sexe
        dimanche_list = Use.filter(participant__titre=u.participant.titre)
        # On retire ceux qui ne sont pas libre dimanche
        dimanche_list = dimanche_list.exclude(user1__tournoi__titre__jour="Dimanche").exclude(
            user2__tournoi__titre__jour="Dimanche")
        querysets.append(dimanche_list)

    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    length = 0
    if len(querysets) > 0:
        # Merge query sets
        Use = reduce(or_, querysets[1:], querysets[0])
        length = len(Use)
        Use = Use[debut - 1:fin]
    else:
        Use = list()

    # calcul des ages des users
    born = request.user.participant.datenaissance
    request.user.age = today.year - born.year

    for u in Use:
        born = u.participant.datenaissance
        u.age = today.year - born.year

    if request.method == "POST":
        if request.POST['action'] == "formPair":
            # On recupère les donnée du formualaire
            username2 = request.POST['username2']
            comment1 = request.POST['remarque']
            title_tournoi = request.POST['title_tournoi']
            categorie_tournoi = request.POST['categorie_tournoi']
            if categorie_tournoi == "-":
                categorie_tournoi = title_tournoi
            # On recupere le tournoi en fonction du titre et de la categorie
            t = TournoiTitle.objects.get(nom=title_tournoi)
            c = TournoiCategorie.objects.get(nom=categorie_tournoi)
            tournois = Tournoi.objects.get(titre=t, categorie=c)
            extra = request.POST.getlist('extra')
            # On recupere les extras pris par l'utilisateur
            extra1 = list()
            for elem in extra:
                extra1.append(Extra.objects.get(id=elem))
            # On en déduit les extras non pris par l'utilisateur
            extranot1 = list()
            Ex = Extra.objects.all()
            for elem in Ex:
                contained = False
                for el in extra1:
                    if elem.id == el.id:
                        contained = True
                if contained == False:
                    extranot1.append(Extra.objects.get(id=elem.id))

            # On vérifie que l'utilisateur a bien rentré un deuxieme joueur
            if (username2 == ""):
                errorAdd = u"Veuillez rajouter un deuxième joueur pour votre pair"
                return render(request, 'inscriptionTournoi.html', locals())

            # On véririe qu'il ne s'est pas entré lui meme
            user1 = User.objects.get(username=request.user.username)
            user2 = User.objects.get(username=username2)

            if (user1 == user2):
                errorAdd = "Vous ne pouvez pas faire une pair avec vous meme"
                return render(request, 'inscriptionTournoi.html', locals())

            # Série de vérification pour que l'utilisateur ou son partenaire ne
            # soit pas inscrit dans un tournoi du meme jour
            user1Tournoi1 = user1.user1.all()
            user1Tournoi2 = user1.user2.all()

            user2Tournoi1 = user2.user1.all()
            user2Tournoi2 = user2.user2.all()

            for elem in user1Tournoi1:
                if(elem.tournoi.titre.jour == tournois.titre.jour):
                    errorAdd = u"Vous êtes déjà inscrit à un tournoi ce jour!"
                    return render(request, 'inscriptionTournoi.html', locals())

            for elem in user1Tournoi2:
                if(elem.tournoi.titre.jour == tournois.titre.jour):
                    errorAdd = u"Vous êtes déjà inscrit à un tournoi ce jour!"
                    return render(request, 'inscriptionTournoi.html', locals())

            for elem in user2Tournoi1:
                if(elem.tournoi.titre.jour == tournois.titre.jour and elem.confirm):
                    errorAdd = u"Le joueur 2 est déjà inscrit dans un tournoi ce jour!"
                    return render(request, 'inscriptionTournoi.html', locals())

            for elem in user2Tournoi2:
                if elem.tournoi.titre.jour == tournois.titre.jour and elem.confirm:
                    errorAdd = u"Le joueur 2 est déjà inscrit dans un tournoi ce jour!"
                    return render(request, 'inscriptionTournoi.html', locals())

            # On crée la pair
            pair = Pair(tournoi=tournois, user1=user1, user2=user2,
                        comment1=comment1, confirm=False, valid=False, pay=False)
            pair.save()
            # On rajoute les extras
            for elem in extra:
                ext = Extra.objects.get(id=elem)
                pair.extra1.add(ext)

            # Send mail
            send_confirmation_email_pair_registered(Participant.objects.get(
                user=pair.user1), Participant.objects.get(user=pair.user2))

            pair.save()
            return redirect(reverse(tournoi))

    if request.user.is_authenticated():
        extranot1 = Extra.objects.all()
        return render(request, 'inscriptionTournoi.html', locals())
    return redirect(reverse(home))
