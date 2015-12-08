# coding: utf-8
'''
Implémentation de l'exportation sous forme de CSV des terrains depuis
l'interface administrateur
'''
from django.http import HttpResponse

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Terrains.csv'
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Rue"),
        smart_str(u"Numéro"),
        smart_str(u"Boîte"),
        smart_str(u"Code postal"),
        smart_str(u"Localité"),
        smart_str(u"Latitude"),
        smart_str(u"Longitude"),
        smart_str(u"Accès"),
        smart_str(u"Surface"),
        smart_str(u"Type"),
        smart_str(u"Samedi"),
        smart_str(u"Dimanche"),
        smart_str(u"Etat"),
        smart_str(u"Comm. propriétaire"),
        smart_str(u"Comm. staff"),
        smart_str(u"Validé"),
        smart_str(u"Username"),
        smart_str(u"email"),
        smart_str(u"Prénom du propriétaire"),
        smart_str(u"Nom du propriétaire"),
        smart_str(u"Utilisé l'année passée"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.id),
            smart_str(obj.rue),
            smart_str(obj.numero),
            smart_str(obj.boite),
            smart_str(obj.codepostal),
            smart_str(obj.localite),
            smart_str(obj.latitude),
            smart_str(obj.longitude),
            smart_str(obj.acces),
            smart_str(obj.matiere.nom),
            smart_str(obj.type.nom),
            smart_str(obj.dispoSamedi),
            smart_str(obj.dispoDimanche),
            smart_str(obj.etat.nom),
            smart_str(obj.commentaire),
            smart_str(obj.commentaireStaff),
            smart_str(obj.valide),
            smart_str(obj.user.username),
            smart_str(obj.user.email),
            smart_str(obj.user.participant.prenom),
            smart_str(obj.user.participant.nom),
            smart_str(obj.usedLastYear),
        ])
    return response
export_csv.short_description = u"Exporter les terrains vers Excel"
