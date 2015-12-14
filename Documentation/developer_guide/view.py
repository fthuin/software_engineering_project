def sponsors(request):
    return render(request, 'sponsors.html', {})

# coding=utf-8
'''
This file contains all the urls available and their links
to a view in views.py
'''
from django.conf.urls import url, patterns

urlpatterns = patterns('tennis.views',
                       url(r'^$', 'home'),
                       url(r'^connexion$', 'connect'),
                       url(r'^deconnexion$', 'deconnect'),
                       url(r'^inscription$', 'register'),
                       url(r'^sponsors$', 'sponsors'),
                       url(r'^contact$', 'contact'),
                       )
