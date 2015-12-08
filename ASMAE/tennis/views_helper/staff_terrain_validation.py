# /usr/bin/env python
# coding: utf8

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import Court, LogActivity
from tennis.views import home

def view(request, id):

    court = Court.objects.get(id=id)
    if request.method == "POST":
        message = request.POST['message']
        if request.POST.__contains__("valide"):
            valide = True
            LogActivity(user=request.user, section="Terrain",
                        details=u"Terrain " + id + u" validé").save()
        else:
            valide = False
            LogActivity(user=request.user, section="Terrain",
                        details=u"Terrain " + id + " désactivé").save()

        court.commentaireStaff = message
        court.valide = valide
        court.save()
        successEdit = "Terrain bien édité!"

    if request.user.is_authenticated():
        return render(request, 'validateTerrain.html', locals())
    return redirect(reverse(home))
