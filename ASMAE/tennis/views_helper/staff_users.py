# /usr/bin/env python
# coding: utf8

from tennis.views import home, yearsago, db_type
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from datetime import date
from django.http import HttpResponse

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
        if request.POST['action'] == "CSV":
            #TODO Florian
            pass
        if request.POST['action'] == "addr_list":
            #TODO Florian export sous CSV la listes de toutes les adresses uniques
            pass

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

    if request.method == 'POST':
        if request.POST['action'] == "CSV":
            import csv
            from django.utils.encoding import smart_str
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Utilisateurs.csv'
            writer = csv.writer(response, csv.excel)
            # BOM (optional...Excel needs it to open UTF-8 file properly)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"Username"),
                smart_str(u"Titre"),
                smart_str(u"Nom"),
                smart_str(u"Prénom"),
                smart_str(u"Rue"),
                smart_str(u"Numéro"),
                smart_str(u"Boite"),
                smart_str(u"Codepostal"),
                smart_str(u"Localité"),
                smart_str(u"Latitude"),
                smart_str(u"Longitude"),
                smart_str(u"Téléphone"),
                smart_str(u"Fax"),
                smart_str(u"GSM"),
                smart_str(u"Date de naissance"),
                smart_str(u"Classement"),
                smart_str(u"Ancien participant"),
                smart_str(u"Classement vérifié"),
                smart_str(u"Compte activé")
            ])
            for obj in Use:
                writer.writerow([
                    smart_str(obj.user.username),
                    smart_str(obj.titre),
                    smart_str(obj.nom),
                    smart_str(obj.prenom),
                    smart_str(obj.rue),
                    smart_str(obj.numero),
                    smart_str(obj.boite),
                    smart_str(obj.codepostal),
                    smart_str(obj.localite),
                    smart_str(obj.latitude),
                    smart_str(obj.longitude),
                    smart_str(obj.telephone),
                    smart_str(obj.fax),
                    smart_str(obj.gsm),
                    smart_str(obj.datenaissance),
                    smart_str(obj.classement),
                    smart_str(obj.oldparticipant),
                    smart_str(obj.isClassementVerified),
                    smart_str(obj.isAccountActivated),
                ])
            return response
        if request.POST['action'] == "addr_list":
            import csv
            from django.utils.encoding import smart_str
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Participants.csv'
            writer = csv.writer(response, csv.excel)
            # BOM (optional...Excel needs it to open UTF-8 file properly)
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([
                smart_str(u"Personnes"),
                smart_str(u"Adresse")
            ])
            adresses_personnes = {}
            for usr in Use:
                if usr.participant.getAdresse() not in adresses_personnes:
                    adresses_personnes[usr.participant.getAdresse()] = usr.participant.fullName()
                else:
                    adresses_personnes[usr.participant.getAdresse()] += u"," +usr.participant.fullName()
            for adresses, personnes in adresses_personnes.iteritems():
                writer.writerow([
                smart_str(adresses),
                smart_str(personnes)
                ])
            return response


    if request.user.is_authenticated():
        return render(request, 'staffUser.html', locals())
    return redirect(reverse(home))
