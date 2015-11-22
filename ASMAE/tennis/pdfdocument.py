# coding=utf-8
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import Color, black, purple, white, yellow, gray, orange

def stylesheet():
    styles= {
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
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
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
        fontSize=14,
        leading=14,
        backColor="#D4542D",
        borderColor="#D4542D",
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
        content = []
        owner_part = [Paragraph('Informations sur le propriétaire', stylesheet['alert'])]
        court_part = [Paragraph('Informations sur le terrain', stylesheet['alert'])]
        creator_part = [Paragraph('Informations sur le membre du staff', stylesheet['alert'])]

        for key, value in owner_content.iteritems():
            owner_part.append(Paragraph(key + ' : ' + value, stylesheet['default']))

        for key, value in court_content.iteritems():
            court_part.append(Paragraph(key + " : " +value, stylesheet['default']))

        for key, value in creator_content.iteritems():
            creator_part.append(Paragraph(key + " : " +value, stylesheet['default']))
        return owner_part + court_part + creator_part

    def build_flowables(self, stylesheet, title, owner_content, court_content, creator_content):
        flowables = []
        flowables.append(buildTitle(stylesheet, title))
        flowables = flowables + self.buildContent(stylesheet, owner_content, court_content, creator_content)
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
        addIfNotNone(owner_content, u'Adresse du propriétaire', owner.codepostal)
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
        addIfNotNone(court_content, u'Accès' , court.acces)
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

        build_pdf(response, self.build_flowables(stylesheet(), 'Terrain '+repr(court.id), owner_content, court_content, creator_content))

class PDFPair():
    def buildContent(self, stylesheet, pair_content, user1_content, user2_content, creator_content):
        pair_part = [Paragraph('Informations sur la paire', stylesheet['alert'])]
        user1_part = [Paragraph('Informations sur le joueur 1', stylesheet['alert'])]
        user2_part = [Paragraph('Informations sur le joueur 2', stylesheet['alert'])]
        creator_part = [Paragraph('Informations sur le membre du staff', stylesheet['alert'])]

        for key, value in pair_content.iteritems():
            pair_part.append(Paragraph(key + " : " +value, stylesheet['default']))

        for key, value in user1_content.iteritems():
            user1_part.append(Paragraph(key + " : " +value, stylesheet['default']))

        for key, value in user2_content.iteritems():
            user2_part.append(Paragraph(key + " : " + value, stylesheet['default']))

        for key, value in creator_content.iteritems():
            creator_part.append(Paragraph(key + ' : ' + value, stylesheet['default']))

        return pair_part + user1_part + user2_part + creator_part

    def build_flowables(self, stylesheet, title, pair_content, user1_content, user2_content, creator_content):
        flowables = []
        flowables.append(buildTitle(stylesheet, title))
        flowables = flowables + self.buildContent(stylesheet, pair_content, user1_content, user2_content, creator_content)
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
        addIfNotNone(user1_content, u'Adresse', pair.user1.participant.codepostal)
        addIfNotNone(user1_content, u'Adresse', ' ')
        addIfNotNone(user1_content, u'Adresse', pair.user1.participant.localite)
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
        addIfNotNone(user2_content, u'Adresse', pair.user2.participant.codepostal)
        addIfNotNone(user2_content, u'Adresse', ' ')
        addIfNotNone(user2_content, u'Adresse', pair.user2.participant.localite)
        addIfNotNone(user2_content, u'GSM', pair.user2.participant.gsm)

        addIfNotNone(pair_content, u'Tournoi', pair.tournoi.nom)
        addIfNotNone(pair_content, u'Commentaire du joueur 1', pair.comment1)
        addIfNotNone(pair_content, u'Commentaire du joueur 2', pair.comment2)

        addIfNotNone(creator_content, u'Nom', userCreator.titre)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.prenom)
        addIfNotNone(creator_content, u'Nom', ' ')
        addIfNotNone(creator_content, u'Nom', userCreator.nom)
        addIfNotNone(creator_content, u'GSM', userCreator.gsm)

        build_pdf(response, self.build_flowables(stylesheet(), 'Paire '+repr(pair.id), pair_content, user1_content, user2_content, creator_content))