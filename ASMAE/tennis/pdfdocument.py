# coding=utf-8
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white, yellow, gray

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
        backColor=gray,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles

def buildTitle(stylesheet, title):
    return Paragraph(title, stylesheet['title'])

def buildContent(stylesheet, owner_content, court_content):
    content = []
    owner_part = [Paragraph('Informations sur le propriétaire', stylesheet['alert'])]
    court_part = [Paragraph('Informations sur le terrain', stylesheet['alert'])]
    
    for key, value in owner_content.iteritems():
        owner_part.append(Paragraph(key, stylesheet['description']))
        owner_part.append(Paragraph(value, stylesheet['default']))
    
    for key, value in court_content.iteritems():
        court_part.append(Paragraph(key, stylesheet['description']))
        court_part.append(Paragraph(value, stylesheet['default']))
    return owner_part + court_part
    
def build_flowables(stylesheet, title, owner_content, court_content):
    flowables = []
    flowables.append(buildTitle(stylesheet, title))
    flowables = flowables + buildContent(stylesheet, owner_content, court_content)
    return flowables


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


class PDFTerrain():
    def __init__(self, response, court, owner):
        owner_content = {}
        court_content = {}
        
        owner_content['Nom'] = owner.nom
        owner_content['Adresse du propriétaire'] = owner.rue + ', ' + owner.numero + ' ' + owner.localite + ' ' + owner.codepostal
        owner_content['Téléphone'] = owner.telephone
        owner_content['GSM'] = owner.gsm
        owner_content['Fax'] = owner.fax
        
        court_content['Adresse du terrain'] = court.rue + ', ' + court.numero + ' ' + court.localite + ' ' + court.codepostal
        court_content['Accès'] = court.acces
        court_content['Surface'] = court.matiere.nom
        court_content['Type'] = court.type.nom
        court_content['Disponibilité'] = ''
        if (court.dispoSamedi and court.dispoDimanche):
            court_content['Disponibilité'] = 'Samedi et dimanche'
        elif (court.dispoSamedi):
            court_content['Disponiblité'] = 'Samedi'
        elif (court.dispoDimanche):
            court_content['Disponibilité'] = 'Dimanche'
        court_content['Etat'] = court.etat.nom
        
        build_pdf(response, build_flowables(stylesheet(), 'Terrain '+repr(court.id), owner_content, court_content))
