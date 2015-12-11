# /usr/bin/env python
# coding: utf8

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tennis.models import LogActivity
from django.db.models import Q
from tennis.views import home

def view(request):

    logs = LogActivity.objects.order_by('-date')
    if request.user.is_authenticated():
        return render(request, 'staffLog.html', locals())
    return redirect(reverse(home))
