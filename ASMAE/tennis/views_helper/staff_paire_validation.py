# /usr/bin/env python
# coding: utf8

from tennis.models import Pair, Tournoi, TournoiCategorie, TournoiTitle, Poule, Extra, LogActivity, infoTournoi
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.views import home, validatePair, staffPaire

def view(request, id):
    pair = Pair.objects.get(id=id)
    paire_logs = LogActivity.objects.filter(section="Paire", target=""+id).order_by('-date')[:10]

    allTournoi = Tournoi.objects.all()

    # Check si la paire fait deja partie d'une poule
    noPoule = True
    for elem in Poule.objects.all():
        if pair in elem.paires.all():
            noPoule = False
            break

    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    today = info.date
    born = pair.user1.participant.datenaissance
    age1 = today.year - born.year - \
        ((today.month, today.day) < (born.month, born.day))

    born = pair.user2.participant.datenaissance
    age2 = today.year - born.year - \
        ((today.month, today.day) < (born.month, born.day))

    if request.method == "POST":
        if request.POST['action'] == "editPair":
            valid = request.POST['valid']
            paid = request.POST['pay']
            tournoi = request.POST['tournoi']
            title = tournoi
            cat = tournoi
            if "_" in tournoi:
                title = tournoi.split("_")[0]
                cat = tournoi.split("_")[1]

            t = TournoiTitle.objects.get(nom=title)
            c = TournoiCategorie.objects.get(nom=cat)
            new_tournoi = Tournoi.objects.get(titre=t, categorie=c)

            if new_tournoi != pair.tournoi:
                pair.tournoi = new_tournoi
                LogActivity(user=request.user, section="Paire", details="Paire " +
                            id + " tournoi = " + str(new_tournoi), target=""+id
                            ).save()
            if valid == "Oui":
                valider = True
                if valider != pair.valid:
                    LogActivity(user=request.user, section="Paire", target=""+id,
                                details=u"Paire validée").save()
            else:
                valider = False
                if valider != pair.valid:
                    LogActivity(user=request.user, section="Paire",target=""+id,
                                details=u"Paire invalidée").save()
            if paid == "Oui":
                payer = True
                if payer != pair.pay:
                    LogActivity(user=request.user, section="Paire",target=""+id,
                                details=u"Paire payée").save()
            else:
                payer = False
                if payer != pair.pay:
                    LogActivity(user=request.user, section="Paire",target=""+id,
                                details=u"Paire non payée").save()
            pair.valid = valider
            pair.pay = payer
            pair.save()
            return redirect(reverse(validatePair, args={id}))

        if request.POST['action'] == "deletePair":
            pair.delete()
            LogActivity(user=request.user, section="Paire", target=""+id,
                        details=u"Paire supprimée").save()
            return redirect(reverse(staffPaire))

    Ex = Extra.objects.all()
    extra1 = pair.extra1.all()
    extranot1 = list()
    for elem in Ex:
        contained = False
        for el in extra1:
            if elem.id == el.id:
                contained = True
        if contained == False:
            extranot1.append(Extra.objects.get(id=elem.id))

    extra2 = pair.extra2.all()
    extranot2 = list()
    for elem in Ex:
        contained = False
        for el in extra2:
            if elem.id == el.id:
                contained = True
        if contained == False:
            extranot2.append(Extra.objects.get(id=elem.id))

    birthdate1 = pair.user1.participant.datenaissance
    formatedBirthdate1 = birthdate1.strftime('%d/%m/%Y')
    birthdate2 = pair.user2.participant.datenaissance
    formatedBirthdate2 = birthdate2.strftime('%d/%m/%Y')
    if request.user.is_authenticated():
        return render(request, 'validatePair.html', locals())
    return redirect(reverse(home))
