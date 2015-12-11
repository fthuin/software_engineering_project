# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet au staff d'encoder les scores relatifs
à une poule
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Poule, PouleStatus, LogActivity, Score, TournoiStatus
from tennis.views import home, pouleTournoi, pouleScore, staffTournoi

def view(request, id):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    poule = Poule.objects.get(id=id)
    if request.method == "POST":
        if request.POST['action'] == 'save':
            poule.status = PouleStatus.objects.get(numero=1)
            poule.save()
        elif request.POST['action'] == 'saveFinite':
            poule.status = PouleStatus.objects.get(numero=2)
            poule.save()
            # Check si toutes les poules sont finite
            valid = True
            for elem in Poule.objects.filter(tournoi=poule.tournoi):
                if elem.status.numero != 2:
                    valid = False
                    break
            if valid:
                t = poule.tournoi
                t.status = TournoiStatus.objects.get(numero=3)
                t.save()
            LogActivity(user=request.user, section="Tournoi", target=""+str(id),
                        details=u"Mise à jour des points de la poule " + str(id) + u" dans le tournoi ").save()
        poule.score.all().delete()
        pairList = poule.paires.all()
        dictionnaire = dict()
        for id1 in pairList:
            for id2 in pairList:
                if (str(id1.id) + "-" + str(id2.id) in dictionnaire) or (str(id2.id) + "-" + str(id1.id) in dictionnaire) or (id1 == id2):
                    pass
                else:
                    dictionnaire[str(id1.id) + "-" + str(id2.id)] = True
                    dictionnaire[str(id2.id) + "-" + str(id1.id)] = True

                    if is_number(request.POST[str(id1.id) + "-" + str(id2.id)]) and is_number(request.POST[str(id2.id) + "-" + str(id1.id)]):
                        score = Score(paire1=id1, paire2=id2, point1=int(request.POST[str(
                            id1.id) + "-" + str(id2.id)]), point2=int(request.POST[str(id2.id) + "-" + str(id1.id)]))
                        score.save()
                        poule.score.add(score)

        if len(poule.score.all()) == 0:
            poule.status = PouleStatus.objects.get(numero=0)
            poule.save()

        if request.POST['action'] == 'save':
            return redirect(reverse(pouleScore, args={id}))
        elif request.POST['action'] == 'saveFinite':
            return redirect(reverse(pouleTournoi, args={poule.tournoi.nom()}))

        return redirect(reverse(staffTournoi))
    if request.user.is_authenticated():
        scoreList = poule.score.all()
        scoreValues = ""
        for sco in scoreList:
            scoreValues = scoreValues + repr(sco.paire1.id) + "-" + repr(sco.paire2.id) + "," + repr(
                sco.point1) + "." + repr(sco.paire2.id) + "-" + repr(sco.paire1.id) + "," + repr(sco.point2) + "."
        scoreValues = scoreValues[:-1]
        return render(request, 'pouleScore.html', locals())
    return redirect(reverse(home))
