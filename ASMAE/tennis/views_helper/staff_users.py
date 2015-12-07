# /usr/bin/env python
# coding: utf8

from tennis.views import home, yearsago, db_type
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from datetime import date

def view(request):
    page = 1
    pageLength = 10
    recherche = ""
    sexe = ""
    age_min = 0
    age_max = 100
    in_paire = ""
    veteran = ""
    if request.method == 'POST':
        page = request.POST['page']
        pageLength = int(request.POST['pagelength'])
        recherche = request.POST['rechercheField'].strip()
        sexe = request.POST['sex_selector']
        in_paire = request.POST['inpair']
        veteran = request.POST['veteran']
        age_min = int(request.POST['agemin'])
        age_max = int(request.POST['agemax'])

    Use = User.objects.all().order_by('username')

    # recherche sexe
    if sexe != "":
        Use = Use.filter(participant__titre=sexe)
    # recherche veteran
    if veteran != "":
        if veteran == "True":
            Use = Use.filter(participant__oldparticipant=True)
        else:
            Use = Use.filter(participant__oldparticipant=False)

    date_min = yearsago(age_min)
    date_max = yearsago(age_max)

    # Recherche age min
    Use = Use.filter(participant__datenaissance__lte=date_min)

    # Recherceh age max
    Use = Use.filter(participant__datenaissance__gte=date_max)

    #recherche in paire
    if in_paire != "":
        if in_paire == "True":
            Use = Use.filter(Q(user1__confirm=True) | Q(user2__confirm=True))
        else:
            Use = Use.filter(
                ~(Q(user1__confirm=True) | Q(user2__confirm=True)))

    # recherche firld
    if recherche != "":
        Use = Use.filter(Q(username__icontains=recherche) | Q(
                participant__nom__icontains=recherche) | Q(participant__prenom__icontains=recherche))

    Use = Use.order_by("username")
    length = len(Use)
    debut = ((int(page) - 1) * pageLength) + 1
    fin = debut + (pageLength - 1)
    Use = Use[debut - 1:fin]

    ageRange = range(0, 100)

    today = date.today()
    for u in Use:
        born = u.participant.datenaissance
        u.age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
        u1_list = u.user1.all()
        u2_list = u.user2.all()
        inPair = False
        for p in u1_list or u2_list:
            if p.confirm:
                inPair = True
                break
        u.inpaire = inPair

    if request.user.is_authenticated():
        return render(request, 'staffUser.html', locals())
    return redirect(reverse(home))
