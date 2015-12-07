# coding=utf-8
'''
Cette classe gère la création de PDF à partir de données sur le serveur en
utilisant reportlab.

Cette classe requiert l'installation de reportlab :
pip install reportlab
'''
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, black, purple, white, yellow, gray, orange

image_deloitte = Image(
    "./tennis/static/tennis/img/sponsors_deloitte.jpg", width=181 / 2, height=87 / 2)
image_eventail = Image(
    "./tennis/static/tennis/img/sponsors_eventail.jpg", width=189 / 2, height=50 / 2)
image_exki = Image("./tennis/static/tennis/img/sponsors_exki.jpg",
                   width=104 / 2, height=105 / 2)
image_hayez = Image(
    "./tennis/static/tennis/img/sponsors_hayez.jpg", width=202 / 2, height=76 / 2)
image_lalibre = Image(
    "./tennis/static/tennis/img/sponsors_lalibre.jpg", width=166 / 2, height=58 / 2)
image_raidillon = Image(
    "./tennis/static/tennis/img/sponsors_raidillon.jpg", width=109 / 2, height=109 / 2)
image_smart = Image(
    "./tennis/static/tennis/img/sponsors_smart.jpg", width=173 / 2, height=69 / 2)
image_vw = Image("./tennis/static/tennis/img/sponsors_VW.jpg",
                 width=111 / 2, height=131 / 2)
image_weplay = Image(
    "./tennis/static/tennis/img/sponsors_weplay.jpg", width=171 / 2, height=45 / 2)


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['description'] = ParagraphStyle(
        'description',
        parent=styles['default'],
        fontName='Times-Roman',
        textTransform='uppercase',
    )
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        #        textColor=purple,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=14,
        backColor="#D4542D",
        borderColor="#BF4C28",
        textColor="#FFFFFF",
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles


def buildTitle(stylesheet, title):
    return Paragraph(title, stylesheet['title'])


def build_pdf(response, flowables):
    doc = BaseDocTemplate(response)
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )
    doc.build(flowables)


def addIfNotNone(dic, ind, value):
    if ind.upper() not in dic:
        dic[ind.upper()] = ''
    if value != None and value != '':
        dic[ind.upper()] += value
    else:
        dic[ind.upper()] += ' - '


class PDFTerrain():

    def buildContent(self, stylesheet, owner_content, court_content, creator_content):
        owner_part = [
            Paragraph('Informations sur le propriétaire', stylesheet['alert'])]
        court_part = [
            Paragraph('Informations sur le terrain', stylesheet['alert'])]
        creator_part = [
            Paragraph('Informations sur le membre du staff', stylesheet['alert'])]

        for key, value in owner_content.iteritems():
            owner_part.append(
                Paragraph(key + ' : ' + value, stylesheet['default']))

        for key, value in court_content.iteritems():
            court_part.append(
                Paragraph(key + " : " + value, stylesheet['default']))

        for key, value in creator_content.iteritems():
            creator_part.append(
                Paragraph(key + " : " + value, stylesheet['default']))
        return owner_part + court_part + creator_part

    def build_flowables(self, stylesheet, title, owner_content, court_content, creator_content):
        flowables = []
        flowables.append(buildTitle(stylesheet, title))
        flowables = flowables + \
            self.buildContent(stylesheet, owner_content,
                              court_content, creator_content)
        return flowables

    def __init__(self, response, court, owner, userCreator):
        owner_content = {}
        court_content = {}
        creator_content = {}

        addIfNotNone(owner_content, u'Nom', owner.titre)
        addIfNotNone(owner_content, u'Nom', ' ')
        addIfNotNone(owner_content, u'Nom', owner.prenom)
        addIfNotNone(owner_content, u'Nom', ' ')
        addIfNotNone(owner_content, u'Nom', owner.nom)
        addIfNotNone(owner_content, u'Adresse du propriétaire', owner.rue)
        addIfNotNone(owner_content, u'Adresse du propriétaire', ', ')
        addIfNotNone(owner_content, u'Adresse du propriétaire', owner.numero)
        addIfNotNone(owner_content, u'Adresse du propriétaire', ' ')
        addIfNotNone(owner_content, u'Adresse du propriétaire', owner.localite)
        addIfNotNone(owner_content, u'Adresse du propriétaire', ' ')
        addIfNotNone(owner_content, u'Adresse du propriétaire',
                     owner.codepostal)
        addIfNotNone(owner_content, u'Téléphone', owner.telephone)
        addIfNotNone(owner_content, u'GSM', owner.gsm)
        addIfNotNone(owner_content, u'Fax', owner.fax)

        addIfNotNone(court_content, u'Adresse du terrain', court.rue)
        addIfNotNone(court_content, u'Adresse du terrain', ', ')
        addIfNotNone(court_content, u'Adresse du terrain', court.numero)
        addIfNotNone(court_content, u'Adresse du terrain', ' ')
        addIfNotNone(court_content, u'Adresse du terrain', court.localite)
        addIfNotNone(court_content, u'Adresse du terrain', ' ')
        addIfNotNone(court_content, u'Adresse du terrain', court.codepostal)
        addIfNotNone(court_content, u'Accès', court.acces)
        addIfNotNone(court_content, u'Surface', court.matiere.nom)
        addIfNotNone(court_content, u'Type', court.type.nom)
        if (court.dispoSamedi and court.dispoDimanche):
            addIfNotNone(court_content, u'Disponibilité', 'Samedi et dimanche')
        elif (court.dispoSamedi):
            addIfNotNone(court_content, u'Disponiblité', 'Samedi')
        elif (court.dispoDimanche):
            addIfNotNone(court_content, u'Disponibilité', 'Dimanche')
        addIfNotNone(court_content, u'Etat', court.etat.nom)

        addIfNotNone(creator_content, u'Nom', userCreator.titre)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.prenom)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.nom)
        addIfNotNone(creator_content, u'GSM', userCreator.gsm)

        build_pdf(response, self.build_flowables(stylesheet(), 'Terrain ' +
                                                 repr(court.id), owner_content, court_content, creator_content))


class PDFPair():

    def buildContent(self, stylesheet, pair_content, user1_content, user2_content, creator_content):
        pair_part = [
            Paragraph('Informations sur la paire', stylesheet['alert'])]
        user1_part = [
            Paragraph('Informations sur le joueur 1', stylesheet['alert'])]
        user2_part = [
            Paragraph('Informations sur le joueur 2', stylesheet['alert'])]
        creator_part = [
            Paragraph('Informations sur le membre du staff', stylesheet['alert'])]

        for key, value in pair_content.iteritems():
            pair_part.append(
                Paragraph(key + " : " + value, stylesheet['default']))

        for key, value in user1_content.iteritems():
            user1_part.append(
                Paragraph(key + " : " + value, stylesheet['default']))

        for key, value in user2_content.iteritems():
            user2_part.append(
                Paragraph(key + " : " + value, stylesheet['default']))

        for key, value in creator_content.iteritems():
            creator_part.append(
                Paragraph(key + ' : ' + value, stylesheet['default']))

        return pair_part + user1_part + user2_part + creator_part

    def build_flowables(self, stylesheet, title, pair_content, user1_content, user2_content, creator_content):
        flowables = []
        flowables.append(buildTitle(stylesheet, title))
        flowables = flowables + \
            self.buildContent(stylesheet, pair_content,
                              user1_content, user2_content, creator_content)
        return flowables

    def __init__(self, response, pair, userCreator):
        pair_content = {}
        user1_content = {}
        user2_content = {}
        creator_content = {}

        addIfNotNone(user1_content, u'Nom', pair.user1.participant.titre)
        addIfNotNone(user1_content, u'Nom', ' ')
        addIfNotNone(user1_content, u'Nom', pair.user1.participant.prenom)
        addIfNotNone(user1_content, u'Nom', ' ')
        addIfNotNone(user1_content, u'Nom', pair.user1.participant.nom)
        addIfNotNone(user1_content, u'Adresse', pair.user1.participant.numero)
        addIfNotNone(user1_content, u'Adresse', ', ')
        addIfNotNone(user1_content, u'Adresse', pair.user1.participant.rue)
        addIfNotNone(user1_content, u'Adresse', ' ')
        addIfNotNone(user1_content, u'Adresse',
                     pair.user1.participant.codepostal)
        addIfNotNone(user1_content, u'Adresse', ' ')
        addIfNotNone(user1_content, u'Adresse',
                     pair.user1.participant.localite)
        addIfNotNone(user1_content, u'GSM', pair.user1.participant.gsm)

        addIfNotNone(user2_content, u'Nom', pair.user2.participant.titre)
        addIfNotNone(user2_content, u'Nom', ' ')
        addIfNotNone(user2_content, u'Nom', pair.user2.participant.prenom)
        addIfNotNone(user2_content, u'Nom', ' ')
        addIfNotNone(user2_content, u'Nom', pair.user2.participant.nom)
        addIfNotNone(user2_content, u'Adresse', pair.user2.participant.numero)
        addIfNotNone(user2_content, u'Adresse', ', ')
        addIfNotNone(user2_content, u'Adresse', pair.user2.participant.rue)
        addIfNotNone(user2_content, u'Adresse', ' ')
        addIfNotNone(user2_content, u'Adresse',
                     pair.user2.participant.codepostal)
        addIfNotNone(user2_content, u'Adresse', ' ')
        addIfNotNone(user2_content, u'Adresse',
                     pair.user2.participant.localite)
        addIfNotNone(user2_content, u'GSM', pair.user2.participant.gsm)

        addIfNotNone(pair_content, u'Tournoi', pair.tournoi.titre.nom)
        addIfNotNone(pair_content, u'Commentaire du joueur 1', pair.comment1)
        addIfNotNone(pair_content, u'Commentaire du joueur 2', pair.comment2)

        addIfNotNone(creator_content, u'Nom', userCreator.titre)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.prenom)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.nom)
        addIfNotNone(creator_content, u'GSM', userCreator.gsm)

        build_pdf(response, self.build_flowables(stylesheet(), 'Paire ' +
                                                 repr(pair.id), pair_content, user1_content, user2_content, creator_content))


def create_poule_table_flowables(poule):
    paires = poule.paires.all()
    poule_table = []
    tableStyle = []
    nbr_pairs = len(paires) + 1
    for i in range(nbr_pairs):
        if i == 0:
            poule_table.append([''])
            for j in range(nbr_pairs - 1):
                poule_table[i].append(paires[j].user1.participant.smallName(
                ) + "\n" + paires[j].user2.participant.smallName())
        else:
            poule_table.append([paires[i - 1].user1.participant.smallName() +
                                "\n" + paires[i - 1].user2.participant.smallName()])
            for j in range(nbr_pairs - 1):
                poule_table[i].append("")
        tableStyle.append(('BACKGROUND', (i, i), (i, i), colors.grey))
        tableStyle.append(
            ("INNERGRID", (0, 0), (i, nbr_pairs - 1), 0, colors.black))
    tableStyle.append(('FONTSIZE', (0, 0), (0, nbr_pairs - 1), 8))
    tableStyle.append(('FONTSIZE', (0, 0), (nbr_pairs - 1, 0), 8))
    t = Table(poule_table)
    t.setStyle(TableStyle(tableStyle))
    return [t]

def create_staff_flowables(stylesheet, staffParticipant):
    staff_part = [
        Paragraph('Informations sur le staff', stylesheet['alert'])]
    nom = staffParticipant.titre + ' ' + \
        staffParticipant.prenom + ' ' + staffParticipant.nom
    gsm = staffParticipant.gsm
    staff_part.append(Paragraph("NOM : " + nom, stylesheet['default']))
    staff_part.append(Paragraph("GSM : " + gsm, stylesheet['default']))
    return staff_part

def create_pairs_flowables(pairs):
    pairs_part = []
    for paire in pairs:
        pairs_part += [Paragraph('Informations sur la paire ' +
                                 str(paire.id), stylesheet()['alert'])]
        paire_part = []
        paire_part.append(["NOM : " + paire.user1.participant.titre + " " + paire.user1.participant.prenom + " " + paire.user1.participant.nom,
                           "NOM : " + paire.user2.participant.titre + " " + paire.user2.participant.prenom + " " + paire.user2.participant.nom])
        paire_part.append(
            ["GSM : " + paire.user1.participant.gsm, "GSM : " + paire.user2.participant.gsm])
        paire_part.append(["CLASSEMENT : " + paire.user1.participant.classement.nom,
                           "CLASSEMENT : " + paire.user2.participant.classement.nom])
        tableStyle = []
        tableStyle.append(('FONTSIZE', (0, 0), (1, 2), 8))
        tableStyle.append(("INNERGRID", (0, 0), (1, 2), 0, colors.black))
        t = Table(paire_part)
        t.setStyle(TableStyle(tableStyle))
        pairs_part.append(t)
    return pairs_part

def create_court_flowables(court, stylesheet):
    court_part = []
    owner_fullname = ""
    if court.user.participant.titre != None:
        owner_fullname += court.user.participant.titre + " "
    if court.user.participant.prenom != None:
        owner_fullname += court.user.participant.prenom + " "
    if court.user.participant.nom != None:
        owner_fullname += court.user.participant.nom
    owner_fax = ""
    if court.user.participant.nom != None and court.user.participant.nom.strip != "":
        owner_fax += court.user.participant.fax
    else:  # NO FAX
        owner_fax += "-"
    owner_gsm = ""
    if court.user.participant.gsm != None and court.user.participant.gsm.strip != "":
        owner_gsm += court.user.participant.gsm
    else:
        owner_gsm += "-"
    owner_telephone = ""
    if court.user.participant.telephone != None and court.user.participant.telephone != "":
        owner_telephone += court.user.participant.telephone
    else:
        owner_telephone += "-"
    owner_part = []
    owner_part = [
        Paragraph('Informations sur le propriétaire', stylesheet['alert'])]
    court_part = [
        Paragraph('Informations sur le terrain', stylesheet['alert'])]
    owner_part.append(
        Paragraph('NOM : ' + owner_fullname, stylesheet['default']))
    owner_part.append(
        Paragraph('FAX : ' + owner_fax, stylesheet['default']))
    owner_part.append(
        Paragraph('GSM : ' + owner_gsm, stylesheet['default']))
    owner_part.append(
        Paragraph('TELEPHONE : ' + owner_telephone, stylesheet['default']))
    owner_part.append(Paragraph('ADRESSE DU PROPRIETAIRE : ' +
                                court.user.participant.getAdresse(), stylesheet['default']))
    court_etat = ""
    if court.etat.nom != None and court.etat.nom.strip != "":
        court_etat += court.etat.nom
    else:
        court_etat += "-"
    court_surface = ""
    if court.matiere.nom != None and court.matiere.nom.strip != "":
        court_surface += court.matiere.nom
    else:
        court_surface += "-"
    court_acces = ""
    if court.acces != None and court.acces.strip != "":
        court_acces += court.acces
    else:
        court_acces += "-"
    court_part.append(
        Paragraph('ETAT : ' + court_etat, stylesheet['default']))
    court_part.append(
        Paragraph('SURFACE : ' + court_surface, stylesheet['default']))
    court_part.append(
        Paragraph('ACCES : ' + court_acces, stylesheet['default']))
    court_part.append(Paragraph('ADRESSE DU TERRAIN : ' +
                                court.getAdresse(), stylesheet['default']))
    return owner_part + court_part

def create_sponsors_flowables():
    sponsors_image = []
    sponsors_image.append([Image("./tennis/static/tennis/img/sponsors_deloitte.jpg", width=181 / 2, height=87 / 2), Image(
        "./tennis/static/tennis/img/sponsors_eventail.jpg", width=189 / 2, height=50 / 2), Image("./tennis/static/tennis/img/sponsors_exki.jpg", width=104 / 2, height=105 / 2)])
    sponsors_image.append([Image("./tennis/static/tennis/img/sponsors_hayez.jpg", width=202 / 2, height=76 / 2), Image("./tennis/static/tennis/img/sponsors_lalibre.jpg",
                                                                                                                       width=166 / 2, height=58 / 2), Image("./tennis/static/tennis/img/sponsors_raidillon.jpg", width=109 / 2, height=109 / 2)])
    sponsors_image.append([Image("./tennis/static/tennis/img/sponsors_smart.jpg", width=173 / 2, height=69 / 2), Image("./tennis/static/tennis/img/sponsors_VW.jpg",
                                                                                                                       width=111 / 2, height=131 / 2), Image("./tennis/static/tennis/img/sponsors_weplay.jpg", width=171 / 2, height=45 / 2)])
    table = Table(sponsors_image)
    return [table]

class PDFPoule():
    def __init__(self, response, poule, staffUser):
        flowables = []
        flowables.append(buildTitle(
            stylesheet(), "Poule " + repr(poule.id)))
        flowables += create_staff_flowables(
            stylesheet(), staffUser.participant)
        flowables.append(
            Paragraph('Tableaux des scores', stylesheet()['alert']))
        flowables += create_poule_table_flowables(poule)
        flowables += create_pairs_flowables(poule.paires.all())
        flowables += create_court_flowables(poule.court, stylesheet())
        flowables += create_sponsors_flowables()
        build_pdf(response, flowables)

class PDF_all_poules():
    def __init__(self, response, list_poules, staff_user):
        flowables = []
        for poule in list_poules:
            flowables.append(buildTitle(
                stylesheet(), "Poule " + repr(poule.id)))
            flowables += create_staff_flowables(
                stylesheet(), staff_user.participant)
            flowables.append(
                Paragraph('Tableaux des scores', stylesheet()['alert']))
            flowables += create_poule_table_flowables(poule)
            flowables += create_pairs_flowables(poule.paires.all())
            flowables += create_court_flowables(poule.court, stylesheet())
            flowables += create_sponsors_flowables()
            flowables += [PageBreak()]
        build_pdf(response, flowables)
