# coding=utf-8

from django.core.mail import send_mail

#send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
# From : noreply@leCharleDeLorraine.com

# Send a confirmation email for pair registration
def send_confirmation_email_pair_registered(participantOne, participantTwo): 
    #Init Mail variable
    playerOnePrenom = participantOne.prenom
    playerOneFullName = participantOne.prenom + " " + participantOne.nom
    playerOneAdresseMail = participantOne.user.email

    playerTwoPrenom = participantTwo.prenom
    playerTwoFullName = participantTwo.prenom + " " + participantTwo.nom
    playerTwoAdresseMail = participantTwo.user.email

    #adresseAsmae = 'noreply@leCharleDeLorraine.com'
    subject = "Confirmation d'inscription au tournoi 'Le charle de Lorraine'"

    messagePlayerOne =  "Bonjour " + playerOnePrenom + """,

    Vous avez été enregistrer pour jouer en pair avec """ + playerTwoFullName + """
    lors du prochain tournoi 'Le Charle de Lorraine'.

    Si ce enregistrement a été fait par erreur, sachez qu'il reste possible de modifier les
    informations d'inscription sur notre site jusqu'a l'avant veille du tournoi. Nous somme
    également disponible en cas de besoin via l'onglet contact du site internet.

    Merci encore de votre inscription,
    L'équipe 'Le charle de Lorraine'
    """

    messagePlayerTwo =  "Bonjour " + playerTwoPrenom + """,

    Vous avez été enregistrer pour jouer en pair avec """ + playerOneFullName + """
    lors du prochain tournoi 'Le Charle de Lorraine'.

    Si ce enregistrement a été fait par erreur, sachez qu'il reste possible de modifier les
    informations d'inscription sur notre site jusqu'a l'avant veille du tournoi. Nous somme
    également disponible en cas de besoin via l'onglet contact du site internet.

    Merci encore de votre inscription,
    L'équipe 'Le charle de Lorraine'
    """

    #Send
    send_mail(subject, messagePlayerOne, "", [playerOneAdresseMail], fail_silently=False)
    send_mail(subject, messagePlayerTwo, "", [playerTwoAdresseMail], fail_silently=False)


# Send a confirmation email for court registration
def send_confirmation_email_court_registered(participant, court):
    #Init Mail variable
    prenom = participant.prenom
    typeCourt = court.type
    adresseCourt = court.rue + " " + court.numero + " " + court.boite + ", " + court.boite + " " + court.localite
    disponibleSamedi = court.dispoSamedi
    disponibleDimanche = court.dispoDimanche
    mail = participant.user.email

    #adresseAsmae = 'noreply@leCharleDeLorraine.com'
    subject = "Confirmation d'enregistrement du terrain"

    message =  "Bonjour " + prenom + """,

    Merci d'avoir prêter votre court de tennis pour le prochain tournoi
    'le charle de lorraine'. Veuillez s'il vous plais re-vérifier que les
    informations ci-dessous correspondent bien a votre terrain.

    Adresse : """ + adresseCourt + """
    Type : """ + typeCourt + """
    Disponibilitée : """

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
    de modifier les informations d'inscription sur notre site. Nous somme également disponible
    en cas de besoin via l'onglet contact du site internet.

    Merci encore de votre soutien,
    L'équipe 'Le charle de Lorraine'
    """

    #Send
    send_mail(subject, message, "", [mail], fail_silently=False)

# TODO methode qui envoie les message des court adresse ou les payment issue selon la situation du client
# A tout les joueurs (excepte les iregularité de payment et les groups leader), envoyé le court sur lequels ils va jouer
def send_email_court_adress():	
    prenom = ""
    mail = "pokcyril@hotmail.com"
    courtAdresse = ""
    subject = "Confirmation d'enregistrement du terrain"
    messagePlayerOne =  "Bonjour " + prenom + """,

    Le tournoi approche a grand pas et l'endroit ou se deroulera
    votre premier match a été décidé. Veuillez donc vous rendre a
    l'adresse suivante :

    """ + courtAdresse + """

    En cas de problème, nous restons disponible via l'onglet contact du site internet.

    Merci encore de votre soutien et bon matchs
    L'équipe 'Le charle de Lorraine'
    """

    send_mail(subject, message, "", [mail], fail_silently=False)


# Envoye a tout les player en irregularite de payment
def send_email_payment_issue():
    prenom = ""
    montant = ""
    adresseHQ = ""
    mail = "pokcyril@hotmail.com"
    subject = "Confirmation d'enregistrement du terrain"

    messagePlayerOne =  "Bonjour " + prenom + """,

    Il semblerais que vous soyez toujours en irregularité de payment pour le tournoi.
    Veuillez donc vous présenter samedi matin afin de régulariser votre situation et
    d'obtenier l'adresse a laquelle vous pourrez jouer. L'adresse du quartier général
    a laquelle vous devez vous présenter ainsi que le montant a fournir peuvent etre
    trouver ci-dessous :

    Montant : """ + montant + """ euros
    Adresse : """ + adresseHQ + """

    En cas de problème, nous restons disponible via l'onglet contact du site internet.

    Merci encore de votre soutien
    L'équipe 'Le charle de Lorraine'
    """

    send_mail(subject, message, "", [mail], fail_silently=False)

# Envoye a tout les groupes leader TODO
def send_email_score_board():
    prenom = ""
    adresseHQ = ""
    mail = "pokcyril@hotmail.com"
    subject = "Confirmation d'enregistrement du terrain"

    messagePlayerOne =  "Bonjour " + prenom + """,

    Pour le prochain tournois vous avez été designer en temps que group leader.
    Nous vous demandons donc de vous présenter le samedi matin a l'adresse ci - dessousa
    afin de recuperer la feuille de cotation. Vous serez également informer de
    l'adresse a laquelle se tiendra votre premier match sur place.

    Adresse : """ + adresseHQ + """

    En cas de problème, nous restons disponible via l'onglet contact du site internet.

    Merci encore de votre soutien
    L'équipe 'Le charle de Lorraine'
    """

    send_mail(subject, message, "", [mail], fail_silently=False)
