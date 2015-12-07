# -*- coding: utf-8 -*-
from django.contrib import admin
from tennis.models import Extra,Participant,Court,Tournoi,Pair, CourtState, CourtSurface, CourtType, LogActivity, Poule, Score, TournoiStatus, PouleStatus, Arbre, TournoiTitle, TournoiCategorie, infoTournoi, Ranking
# Register your models here.
from dump_table import participant, court

class ParticipantAdmin(admin.ModelAdmin):
    actions = [participant.export_csv]
    list_display = ('titre', 'nom', 'prenom', 'rue', 'numero', 'codepostal', 'telephone', 'fax', 'gsm', 'datenaissance', 'classement', 'oldparticipant', 'localite', 'isAccountActivated')
    list_display_links = ('nom',)
    list_filter = ('titre', 'isAccountActivated')
    ordering = ('nom',)
    search_fields = ('titre', 'nom', 'prenom', 'rue', 'numero', 'codepostal', 'telephone', 'fax', 'gsm', 'datenaissance', 'oldparticipant', 'localite')

class ExtraAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix')
    ordering = ('nom',)
    search_fields = ('nom', 'prix', 'commentaires')
    list_editable = ('prix',)

class PairAdmin(admin.ModelAdmin):
    def first_fullname(self, obj):
        return obj.user1.participant.codeName()
    first_fullname.short_description = 'Joueur 1'
    def second_fullname(self, obj):
        return obj.user2.participant.codeName()
    second_fullname.short_description = 'Joueur 2'

    list_display = ('id', 'first_fullname', 'second_fullname', 'confirm', 'valid', 'pay')
    ordering = ('id',)
    list_filter = ['confirm', 'valid', 'pay']
    search_fields = ['id', 'user1__participant__prenom', 'user1__participant__nom', 'user2__participant__prenom', 'user2__participant__nom', 'user1__username', 'user2__username']

class CourtAdmin(admin.ModelAdmin):
    def owner_fullname(self, obj):
        return obj.user.participant.codeName()
    owner_fullname.short_description = 'Propriétaire'

    actions = [court.export_csv]
    list_display = ['id', 'owner_fullname', 'rue', 'numero', 'codepostal', 'localite', 'matiere', 'type', 'dispoSamedi', 'dispoDimanche', 'etat', 'valide', 'usedLastYear']
    ordering = ('id',)
    list_filter = ['matiere', 'type', 'etat', 'dispoSamedi', 'dispoDimanche', 'valide', 'usedLastYear']
    search_fields = ['user__username', 'user__participant__prenom', 'user__participant__nom', 'rue', 'numero', 'localite', 'codepostal']

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
    list_filter = ['section']

class PouleAdmin(admin.ModelAdmin):
    def leader_fullname(self, obj):
        try:
            return obj.leader.participant.codeName()
        except AttributeError:
            return 'Non défini'
    leader_fullname.short_description = 'Leader'
    list_display = ('id', 'tournoi', 'leader_fullname', 'court')
    ordering = ('id',)
    search_fields = ['id', 'leader__participant__prenom', 'leader__participant__nom', 'leader__username', 'court__rue', 'court__localite', 'court__codepostal']

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
admin.site.register(infoTournoi)
admin.site.register(Ranking)
