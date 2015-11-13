# -*- coding: utf-8 -*- 
import datetime
import time
from django.utils.crypto import get_random_string
import threading
from django.core.mail import send_mail
from tennis.models import Extra, Participant,Court, Tournoi, Pair, UserInWaitOfActivation, Poule

#send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
# From : noreply@leCharleDeLorraine.com

def send_mail_via_thread(subject, message, fromAdresse, mailingList, fail_silently=True):
	threading.Thread(target=send_mail, args=(subject, message, fromAdresse, mailingList, fail_silently, )).start()

# Send a confirmation email for pair registration
def send_confirmation_email_pair_registered(participantOne, participantTwo): 
    #Init Mail variable
    playerOneFullName =  participantOne.fullName()
    playerOneAdresseMail = participantOne.user.email

    playerTwoFullName =  participantOne.fullName()
    playerTwoAdresseMail = participantTwo.user.email

    #adresseAsmae = 'noreply@leCharleDeLorraine.com'
    subject = u"Confirmation d'inscription au tournoi 'Le Charles de Lorraine'"

    messagePlayerOne =  u"Bonjour " + playerOneFullName+ u""",

Vous avez été enregistré pour jouer en paire avec """ + playerTwoFullName + u"""
lors du prochain tournoi 'Le Charle de Lorraine'.

Si cet enregistrement a été fait par erreur, sachez qu'il reste possible de modifier les
informations d'inscription sur notre site jusqu'à l'avant veille du tournoi. Nous sommes
également disponible en cas de besoin via l'onglet contact du site internet.

Merci encore de votre inscription,
L'équipe 'Le Charles de Lorraine'
"""

    messagePlayerTwo =  u"Bonjour " + playerTwoFullName + u""",

Vous avez été enregistré pour jouer en paire avec """ + playerOneFullName + u"""
lors du prochain tournoi 'Le Charles de Lorraine'.

Si cet enregistrement a été fait par erreur, sachez qu'il reste possible de modifier les
informations d'inscription sur notre site jusqu'à l'avant veille du tournoi. Nous sommes
également disponible en cas de besoin via l'onglet contact du site internet.

Merci encore de votre inscription,
L'équipe 'Le Charles de Lorraine'
"""

    #Send
    send_mail_via_thread(subject, messagePlayerOne, "", [playerOneAdresseMail])
    send_mail_via_thread(subject, messagePlayerTwo, "", [playerTwoAdresseMail])


# Send a confirmation email for court registration
def send_confirmation_email_court_registered(participant, court):
    #Init Mail variable
    fullName = participant.fullName()
    typeCourt = court.type.nom
    adresseCourt = court.rue + " " + court.numero + " " + court.boite + ", " + court.boite + " " + court.localite
    disponibleSamedi = court.dispoSamedi
    disponibleDimanche = court.dispoDimanche
    mail = participant.user.email

    #adresseAsmae = 'noreply@leCharleDeLorraine.com'
    subject = u"Confirmation d'enregistrement du terrain"

    message =  u"Bonjour " + fullName + u""",

Merci d'avoir mis à disposition votre terrain de tennis pour le prochain tournoi
'Le Charles de Lorraine'. Veuillez s'il vous plait re-vérifier que les
informations ci-dessous correspondent bien à votre terrain.

Adresse : """ + adresseCourt + """
Type : """ + typeCourt + """
Disponibilité : """

    if disponibleDimanche and disponibleSamedi:
        message += "samedi et dimanche"
    elif disponibleDimanche:
        message += "uniquement le dimanche"
    elif disponibleSamedi:
        message += "uniquement le samedi"
    else:
        message += "non disponible"

    message += """

Si une quelconque erreur reste présente dans l'enregistrement, sachez qu'il reste possible
de modifier les informations d'inscription sur notre site. Nous sommes également disponible
en cas de besoin via l'onglet contact du site internet.

Merci encore de votre soutien,
L'équipe 'Le Charles de Lorraine'
"""

    #Send
    send_mail_via_thread(subject, message, "", [mail])


# A tout les joueurs (excepte les iregularité de payment et les groups leader), envoyé le court sur lequels ils va jouer
def send_email_court_adress(participant, court, staff):
    fullName = participant.fullName()
    staffName = staff.fullName()
    #mail = participant.user.email
    mail = "cyril.devogelaere@student.uclouvain.be" # For tests
    courtAdresse = court.getAdresse()
    subject = u"Le Charles de Lorraine : emplacement de votre premier match"
    message =  u"Bonjour " + fullName + u""",

Le tournoi approche à grand pas et l'endroit où se deroulera
votre premier match a été décidé. Veuillez donc vous rendre a
l'adresse suivante :

""" + courtAdresse + u"""

En cas de problème, nous restons disponible via l'onglet contact du site internet.

Merci encore de votre soutien et bons matchs,
""" + staffName + " " + """ de l'équipe 'Le charle de Lorraine'
"""

    send_mail(subject, message, "", [mail], fail_silently=False)


# Envoye a tout les player en irregularite de payment
def send_email_payment_issue(participant, extras, staff):
    fullName = participant.fullName()
    staffName = staff.fullName()
    montant = 20
    for extra in extras:
        montant += extra.prix
    adresseHQ = "5 Place des Carabiniers, 1030 Bruxelles"
    #mail = participant.user.email
    mail = "cyril.devogelaere@student.uclouvain.be" # For tests
    subject = u"Le Charles de Lorraine : Problème de payment"

    message =  u"Bonjour " + fullName + u""",

Il semblerait que vous soyez toujours en irrégularité de payment pour le tournoi.
Veuillez donc vous présenter samedi matin afin de régulariser votre situation et
d'obtenier l'adresse a laquelle vous pourrez jouer. L'adresse du quartier général
a laquelle vous devez vous présenter ainsi que le montant a fournir peuvent etre
trouver ci-dessous :

Montant : """ + str(montant) + u""" euros
Adresse : """ + adresseHQ + u"""

En cas de problème, nous restons disponible via l'onglet contact du site internet.

Merci encore de votre soutien
""" + staffName + " " + """ de l'équipe 'Le charle de Lorraine'
"""

    send_mail(subject, message, "", [mail], fail_silently=False)
	
def send_register_confirmation_email(activationObject, participant, link): 
	fullName = participant.fullName()
	mail = participant.user.email
	subject = "Le Charles de Lorraine : validation de votre adresse email"
	lien = link + activationObject.confirmation_key # http://domain/tennis/emailValidation/confirmation_key
	
	message = u"Bonjour " + fullName + u""",
Afin de finaliser la création de votre compte 'Le Charles de Lorraine',  merci de cliquer sur le lien suivant.

""" + lien + u"""
	
Merci de votre cooperation, 
L'équipe 'Le Charles de Lorraine'
"""
	
	send_mail_via_thread(subject, message, "", [mail])

# Envoye a tout les groupes leader TODO
def send_email_score_board(participant, staff):
    fullName = participant.fullName()
    staffName = staff.fullName()
    adresseHQ = "5 Place des Carabiniers, 1030 Bruxelles"
    #mail = participant.user.email
    mail = "cyril.devogelaere@student.uclouvain.be" # For tests
    subject = u"Le Charles de lorraine : récuperation de la feuille de résultats"

    message =  u"Bonjour " + fullName + u""",
	
Pour le prochain tournoi vous avez été designé en tant que leader de groupe.
Nous vous demandons donc de vous présenter le samedi matin a l'adresse ci dessous
afin de recuperer la feuille de cotation. Vous serez également informer de
l'adresse à laquelle se tiendra votre premier match sur place.

Adresse : """ + adresseHQ + u"""

En cas de problème, nous restons disponible via l'onglet contact du site internet.

Merci encore de votre soutien
""" + staffName + " " + """ de l'équipe 'Le charle de Lorraine'
"""

    send_mail(subject, message, "", [mail], fail_silently=False)

def choose_mail_start_tournament(pair, participant, extras, staff):
    if(not pair.pay):
        # Payment issue
        send_email_payment_issue(participant, extras, staff)
    elif(participant.isGroupLeader):
        # Group leader (people with payement issue are not chosen as group leader as their participation is not guaranteed)
        send_email_score_board(participant, staff)
    else:
        #Default
        court = None
        for poule in Poule.objects.all():
            if pair in poule.paires.all():
                court = poule.court
                break
        if not court == None:
            send_email_court_adress(participant, court, staff)

def thread_send_email_start_tournament(staff):
    for pair in Pair.objects.all():
        choose_mail_start_tournament(pair, Participant.objects.get(user=pair.user1), pair.extra1.all(), staff)
        choose_mail_start_tournament(pair, Participant.objects.get(user=pair.user2), pair.extra2.all(), staff)
        time.sleep(5)

def send_email_start_tournament(staff):
    threading.Thread(target=thread_send_email_start_tournament, args=(staff, )).start()

def test_send_mail():
	staff = Participant.objects.get(nom="istrateur", prenom="Admin")
	thread_send_email_start_tournament(staff)
    
def send_prospectus_by_mail(participant):
	#TODO Envoye un mail contenant les pdf devant etre envoyer. Ne pas créer de pdf dupliquer pour les adresses equivalentes
	pass

def send_invitation_to_player_of_previous_year(participant):
	#TODO Envoye un mail aux joueurs ayant participer les années précédentes
	pass
