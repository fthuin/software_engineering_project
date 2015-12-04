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
        smart_str(u"Username"),
        smart_str(u"Titre"),
        smart_str(u"Nom"),
        smart_str(u"Prénom"),
        smart_str(u"Rue"),
        smart_str(u"Numéro"),
        smart_str(u"Boite"),
        smart_str(u"Codepostal"),
        smart_str(u"Localité"),
        smart_str(u"Latitude"),
        smart_str(u"Longitude"),
        smart_str(u"Téléphone"),
        smart_str(u"Fax"),
        smart_str(u"GSM"),
        smart_str(u"Date de naissance"),
        smart_str(u"Classement"),
        smart_str(u"Ancien participant"),
        smart_str(u"Classement vérifié"),
        smart_str(u"Compte activé")
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.user.username),
            smart_str(obj.titre),
            smart_str(obj.nom),
            smart_str(obj.prenom),
            smart_str(obj.rue),
            smart_str(obj.numero),
            smart_str(obj.boite),
            smart_str(obj.codepostal),
            smart_str(obj.localite),
            smart_str(obj.latitude),
            smart_str(obj.longitude),
            smart_str(obj.telephone),
            smart_str(obj.fax),
            smart_str(obj.gsm),
            smart_str(obj.datenaissance),
            smart_str(obj.classement),
            smart_str(obj.oldparticipant),
            smart_str(obj.isClassementVerified),
            smart_str(obj.isAccountActivated),
        ])
    return response
export_csv.short_description = u"Export Participants in CSV"
