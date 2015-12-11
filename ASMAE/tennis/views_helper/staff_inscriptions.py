# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet au staff de gérer les extras, les frais
d'inscription, la date de tournoi,...
'''

from itertools import chain
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Extra, LogActivity, infoTournoi
from tennis.views import home, resetDbForNextYear
import datetime

def view(request):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    logs_inscription = LogActivity.objects.filter(section="InfoTournoi")
    logs_inscription = logs_inscription | LogActivity.objects.filter(section="Extra")
    logs_inscription = logs_inscription.order_by('-date')[:15]

    extras = Extra.objects.all()
    info = infoTournoi.objects.all()
    info = info.order_by("edition")[len(info) - 1]
    prix_inscription = info.prix
    date_inscription = info.date
    formated_date = date_inscription.strftime('%d/%m/%Y')
    yearLoop = range(datetime.date.today().year, datetime.date.today().year + 5)
    isAdmin = request.user.groups.filter(name="Admin").exists()

    if request.method == "POST":
        if request.POST['action'] == "cleanDb":
            resetDbForNextYear(request)

        if request.POST['action'] == "modifyInfoTournoi":
            prixTournoi = request.POST['prixInscription'].strip()
            dateInfoTournoi = request.POST['birthdate'].strip()

            info = infoTournoi.objects.all()
            info = info.order_by("edition")[len(info) - 1]
            prixTournoi = prixTournoi.replace(",", ".")
            if(float(prixTournoi) >= 0.0):
                info.prix = prixTournoi
                LogActivity(user=request.user, section="InfoTournoi", target=""+repr(info.edition),
                            details=u"Prix de l'édition "+ repr(info.edition) + u" modifié").save()
            else:
                errorInfoPrix = u"Le prix doit être plus grand ou égal a zéro"

            splitedDateInfoTournoi = dateInfoTournoi.split("/")
            datetoEnreg = datetime.datetime(int(splitedDateInfoTournoi[2]), int(
                splitedDateInfoTournoi[1]), int(splitedDateInfoTournoi[0]))
            now = datetime.datetime.now()
            if(now < datetoEnreg):
                info.date = datetoEnreg
                LogActivity(user=request.user, section="InfoTournoi", target=""+repr(info.edition),
                            details=u"Date de l'edition " + repr(info.edition) +u" modifiée").save()
            else:
                errorInfoDate = u"La date doit être plus tard que maintenant"

            info.save()
            info = infoTournoi.objects.all()
            info = info.order_by("edition")[len(info) - 1]
            prix_inscription = info.prix
            date_inscription = info.date
            formated_date = date_inscription.strftime('%d/%m/%Y')
            return render(request, 'staffExtra.html', locals())

        if request.POST['action'] == "addExtra":
            nom = request.POST['name'].strip()
            prix = request.POST['price'].strip()
            message = request.POST['message'].strip()

            if nom == "":
                errorAdd = "Veuillez rajouter un nom à l'extra!"
                return render(request, 'staffExtra.html', locals())

            if not is_number(prix):
                prix = prix.replace(",", ".")
                if not is_number(prix):
                    errorAdd = "Le prix n'a pas le bon format"
                    return render(request, 'staffExtra.html', locals())

            extra = Extra(nom=nom, prix=prix, commentaires=message)
            extra.save()
            LogActivity(user=request.user, section="Extra", target=""+repr(extra.id),
                        details=u"Extra " + nom + u" ajouté").save()

            successAdd = u"Extra " + nom + u" bien ajouté!"

        if request.POST['action'] == "modifyExtra":
            id = request.POST['id']
            nom = request.POST['name']
            prix = request.POST['price']
            message = request.POST['message']

            extra = Extra.objects.get(id=id)

            if nom == "":
                errorEdit = u"Veuillez rajouter un nom à l'extra!"
                return render(request, 'staffExtra.html', locals())

            if not is_number(prix):
                prix = prix.replace(",", ".")
                if not is_number(prix):
                    errorEdit = u"Le prix n'a pas le bon format"
                    return render(request, 'staffExtra.html', locals())

            extra.nom = nom
            extra.prix = prix
            extra.commentaires = message
            extra.save()
            LogActivity(user=request.user, section="Extra", target=""+repr(extra.id),
                        details=u"Extra " + nom + u" modifié").save()
            successEdit = u"Extra " + nom + u" bien modifié !"

        if request.POST['action'] == "deleteExtra":
            id = request.POST['id']
            extra = Extra.objects.get(id=id)
            extra.delete()
            LogActivity(user=request.user, section="Extra",target=""+repr(extra.id),
                        details=u"Extra " + extra.nom + u" supprimé").save()
            successDelete = u"Extra bien supprimé!"

    extras = Extra.objects.all()

    for e in extras:
        a = len(Extra.objects.filter(id=e.id, extra1__valid=True)) + \
            len(Extra.objects.filter(id=e.id, extra2__valid=True))
        e.count = a

    if request.user.is_authenticated():
        return render(request, 'staffExtra.html', locals())
    return redirect(reverse(home))
