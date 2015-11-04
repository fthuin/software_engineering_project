from django.contrib import admin
from tennis.models import Extra,Participant,Court,Tournoi,Pair,Groupe, Match
# Register your models here.
admin.site.register(Participant)
admin.site.register(Extra)
admin.site.register(Court)
admin.site.register(Tournoi)
admin.site.register(Pair)
admin.site.register(Groupe)
admin.site.register(Match)
