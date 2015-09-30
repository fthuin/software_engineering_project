from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('tennis.views',
	url(r'^$','home'),
)