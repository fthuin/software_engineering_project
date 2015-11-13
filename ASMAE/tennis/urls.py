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
	url(r'^tournoi$','tournoi'),
	url(r'^emailValidation/(\w+)$', 'emailValidation'),
	url(r'^tournoi/inscriptionTournoi$','inscriptionTournoi'),
	url(r'^tournoi/confirmer/Pair/(\d+)$','confirmPair'),
	url(r'^tournoi/demande/Pair/(\d+)$','cancelPair'),
	url(r'^tournoi/pair/(\d+)$','viewPair'),
	url(r'^tournoi/payer/pair/(\d+)$','payPair'),
	url(r'^terrain$','terrain'),
	url(r'^terrain/enregistrement$','registerTerrain'),
	url(r'^terrain/edit/(\d+)$','editTerrain'),
	url(r'^staff/tournois$','staffTournoi'),
	url(r'^staff/tournois/([\w ]+)$','generatePool'),
	url(r'^staff/tournois/poules/([\w ]+)$','pouleTournoi'),
	url(r'^staff/tournois/poules/scores/(\d+)$','pouleScore'),
	url(r'^staff/tournois/knockoff/([\w ]+)$','knockOff'),
	url(r'^staff/terrains$','staffTerrain'),
	url(r'^staff/terrains/(\d+)$','validateTerrain'),
	url(r'^staff/terrains/(\d+)/edit/$','editTerrainStaff'),
	url(r'^staff/terrains/(\d+)/pdf/$','terrainPDF'),
	url(r'^staff/paires$','staffPaire'),
	url(r'^staff/paires/(\d+)$','validatePair'),
	url(r'^staff/extras$','staffExtra'),
	url(r'^staff/utilisateurs$','staffUser'),
	url(r'^staff/utilisateurs/(\w+)$','viewUser'),
	url(r'^staff/historique$','staffLog'),
	url(r'^staff/permissions$','staffPerm'),
	url(r'404','qcq'),
)
