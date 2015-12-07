# /usr/bin/env python
# coding: utf8

# coding: utf-8
from django.http import HttpResponse

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Participants.csv'
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Tournoi"),
        smart_str(u"Catégorie"),
        smart_str(u"Joueur 1"),
        smart_str(u"Joueur 2"),
        smart_str(u"Confirmation"),
        smart_str(u"Validation"),
        smart_str(u"Paiement"),
        smart_str(u"Extra joueur 1"),
        smart_str(u"Extra joueur 2")
    ])
    for obj in queryset:
        extra_joueur_1 = ""
        for ex_joueur1 in obj.extra1.all():
            extra_joueur_1 += ex_joueur1.nom + " "
        extra_joueur_2 = ""
        for ex_joueur2 in obj.extra2.all():
            extra_joueur_2 += ex_joueur2.nom + " "
        writer.writerow([
            smart_str(obj.id),
            smart_str(obj.tournoi.titre.nom),
            smart_str(obj.tournoi.categorie.nom),
            smart_str(obj.user1.participant.codeName()),
            smart_str(obj.user2.participant.codeName()),
            smart_str(obj.confirm),
            smart_str(obj.valid),
            smart_str(obj.pay),
            smart_str(extra_joueur_1.strip()),
            smart_str(extra_joueur_2.strip())
        ])
    return response
export_csv.short_description = u"Exporter les paires vers Excel"
