# /usr/bin/env python
# coding: utf8
'''
Implémentation de la view permettant au staff de voir les informations sur
un terrain ainsi que d'ajouter des commentaires et de modifier la validité du
terrain.
'''

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Court, LogActivity
from tennis.views import home

def view(request, id):
    terrain_logs = LogActivity.objects.filter(section="Terrain", target=""+id).order_by('-date')[:10]
    court = Court.objects.get(id=id)
    if request.method == "POST":
        message = request.POST['message']
        if request.POST.__contains__("valide"):
            valide = True
            LogActivity(user=request.user, section="Terrain", target=""+id,
                        details=u"Terrain validé").save()
        else:
            valide = False
            LogActivity(user=request.user, section="Terrain", target=""+id,
                        details=u"Terrain désactivé").save()

        court.commentaireStaff = message
        court.valide = valide
        court.save()
        successEdit = "Terrain bien édité!"

    if request.user.is_authenticated():
        return render(request, 'validateTerrain.html', locals())
    return redirect(reverse(home))
