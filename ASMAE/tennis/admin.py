# -*- coding: utf-8 -*-
from django.contrib import admin
from tennis.models import Extra,Participant,Court,Tournoi,Pair,Groupe
# Register your models here.

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nom', 'prenom', 'rue', 'numero', 'codepostal', 'telephone', 'fax', 'gsm', 'datenaissance', 'classement', 'oldparticipant', 'localite')
    list_display_links = ('nom',)
    list_filter = ('titre',)
    ordering = ('nom',)
    search_fields = ('titre', 'nom', 'prenom', 'rue', 'numero', 'codepostal', 'telephone', 'fax', 'gsm', 'datenaissance', 'classement', 'oldparticipant', 'localite')
    
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix')
    ordering = ('nom',)
    search_fields = ('nom', 'prix', 'commentaires')
    list_editable = ('prix',)
    
class PairAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'confirm', 'valid', 'pay')
    ordering = ('id',)
    
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Court)
admin.site.register(Tournoi)
admin.site.register(Pair, PairAdmin)
admin.site.register(Groupe)
