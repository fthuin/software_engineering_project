# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view qui permet d'encoder les scores relatifs à une
poule.
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Poule, PouleStatus, Score
from tennis.views import home, tournoi

def view(request, id):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    poule = Poule.objects.get(id=id)
    if request.method == "POST":
        poule.status = PouleStatus.objects.get(numero=1)
        poule.save()
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
        return redirect(reverse(tournoi))

    if request.user.is_authenticated():
        scoreList = poule.score.all()
        scoreValues = ""
        for sco in scoreList:
            scoreValues = scoreValues + repr(sco.paire1.id) + "-" + repr(sco.paire2.id) + "," + repr(
                sco.point1) + "." + repr(sco.paire2.id) + "-" + repr(sco.paire1.id) + "," + repr(sco.point2) + "."
        scoreValues = scoreValues[:-1]
        return render(request, 'playerScore.html', locals())
    return redirect(reverse(home))
