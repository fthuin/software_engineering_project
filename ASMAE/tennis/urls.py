from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('tennis.views',
	url(r'^$','home'),
	url(r'^connexion$', 'connect'),
	url(r'^deconnexion$', 'deconnect'),
	url(r'^inscription$','register'),
	url(r'^recuperation$','recover'),
	url(r'^profil$','profil'),
	url(r'^sponsors$','sponsors'),
	url(r'^contact$','contact'),
	url(r'^tournois$','tournoi'),
	url(r'^inscriptionTournoi$','inscriptionTournoi'),
	url(r'^tournoi/confirmPairNUMERO$','confirmPair'),
	url(r'^tournoi/pairNUMERO$','viewPair'),
	url(r'^tournoi/payer/pairNUMERO$','payPair'),
	url(r'^terrain$','terrain'),
	url(r'^terrain/enregistrement$','registerTerrain'),
	url(r'^terrain/edit/(\d+)$','editTerrain'),
	url(r'^staff$','staff'),
	url(r'^staff/terrain/(\d+)$','validateTerrain'),
	url(r'^staff/edit/terrain/(\d+)$','editTerrainStaff'),
)
