# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet de gérer les permissions pour le staff
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import User
from django.db.models import Q
from tennis.views import home, db_type
from tennis.models import TournoiTitle, LogActivity

def view(request):
    page = 1
    pageLength = 10
    recherche = ""
    if request.method == "POST":
        if request.POST['action'] == "search":
            page = request.POST['page']
            recherche = request.POST['rechercheField'].strip()
        else:
            usernamefield = request.POST['username']
            utilisateur = User.objects.get(username=usernamefield)
            staff = False
            if request.POST.__contains__("Tournoi des familles"):
                perm = Permission.objects.get(codename="TournoiDesFamilles")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="TournoiDesFamilles")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("Double mixte"):
                perm = Permission.objects.get(codename="DoubleMixte")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="DoubleMixte")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("Double hommes"):
                perm = Permission.objects.get(codename="DoubleHommes")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="DoubleHommes")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("Double femmes"):
                perm = Permission.objects.get(codename="DoubleFemmes")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="DoubleFemmes")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("court"):
                perm = Permission.objects.get(codename="Court")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="Court")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("pair"):
                perm = Permission.objects.get(codename="Pair")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="Pair")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("extra"):
                perm = Permission.objects.get(codename="Extra")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="Extra")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("user"):
                perm = Permission.objects.get(codename="User")
                utilisateur.user_permissions.add(perm)
                staff = True
            else:
                perm = Permission.objects.get(codename="User")
                utilisateur.user_permissions.remove(perm)

            if request.POST.__contains__("perm"):
                group = Group.objects.get(name="Admin")
                utilisateur.groups.add(group)
            else:
                group = Group.objects.get(name="Admin")
                utilisateur.groups.remove(group)

            if staff:
                group = Group.objects.get(name="staff")
                utilisateur.groups.add(group)
            else:
                group = Group.objects.get(name="staff")
                utilisateur.groups.remove(group)

            LogActivity(user=request.user, section="Permissions",
                        details="Changed permission of user " + utilisateur.username).save()

    Use = User.objects.all().order_by('username')

    if recherche != "":
        if db_type == "postgresql":
            Use = Use.filter(
                Q(username__unaccent__icontains=recherche) |
                Q(participant__nom__unaccent__icontains=recherche) |
                Q(participant__prenom__unaccent__icontains=recherche))
        else:
            Use = Use.filter(
                Q(username__icontains=recherche) |
                Q(participant__nom__icontains=recherche) |
                Q(participant__prenom__icontains=recherche))

    Use = Use.order_by("username")
    length = len(Use)
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    Use = Use[debut - 1:fin]
    tournoiAll = TournoiTitle.objects.all()

    for u in Use:
        bd = u.participant.datenaissance
        fb = bd.strftime('%d/%m/%Y')
        u.fb = fb
    if request.user.is_authenticated():
        return render(request, 'staffPerm.html', locals())
    return redirect(reverse(home))
