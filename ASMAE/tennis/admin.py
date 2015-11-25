# -*- coding: utf-8 -*-
from django.contrib import admin
from tennis.models import Extra,Participant,Court,Tournoi,Pair, CourtState, CourtSurface, CourtType, LogActivity, Poule, Score, TournoiStatus, PouleStatus, Arbre, TournoiTitle, TournoiCategorie
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
    
class CourtAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rue', 'numero', 'codepostal', 'localite', 'matiere', 'type', 'dispoSamedi', 'dispoDimanche', 'etat', 'valide')
    ordering = ('id',)
    
class CourtStateAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    ordering = ('nom',)
    
class CourtSurfaceAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    ordering = ('nom',)

class CourtTypeAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    ordering = ('nom',)
    
class LogActivityAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'section', 'details')
    ordering = ('date',)
    
class PouleAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournoi', 'leader', 'court')
    ordering = ('id',)
    
class TournoiAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre','categorie')

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Court, CourtAdmin)
admin.site.register(TournoiTitle)
admin.site.register(TournoiCategorie)
admin.site.register(Tournoi, TournoiAdmin)
admin.site.register(Pair, PairAdmin)
admin.site.register(Poule, PouleAdmin)
admin.site.register(Score)
admin.site.register(Arbre)
admin.site.register(TournoiStatus)
admin.site.register(PouleStatus)
admin.site.register(LogActivity, LogActivityAdmin)
admin.site.register(CourtState, CourtStateAdmin)
admin.site.register(CourtSurface, CourtSurfaceAdmin)
admin.site.register(CourtType, CourtTypeAdmin)