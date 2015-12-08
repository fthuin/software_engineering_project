# -*- coding: utf-8 -*- 
import sys
import time
import datetime
import sendgrid
import threading
import traceback
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from tennis.models import Extra, Participant, Court, Tournoi, Pair, UserInWaitOfActivation, Poule

#Variables
SENDGRID_USERNAME = "Asmae"
SENDGRID_PASSWORD = "LeCharleDeLorraine2016"
SENDGRID_API_KEY = "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"
CONTACT_EMAIL = "noreply.lecharledelorraine@gmail.com"
EMAIL_FROM = "noreply@lecharledelorraine.com"
#CONTACT_EMAIL_PASSWORD = "LeCharleDeLorraine" KEEP TO CONNECT TO THE MAIL, USELESS IN APP
#EMAIL SENDGRID => pas toucher la cle API sinon faut en recrée une

# MAIL FUNCTION:
def readTemplateFile(fileName):
	# The two next line allows the program to avoid encoding error on some OS, don't touch
	reload(sys)
	sys.setdefaultencoding('utf8')
	try:
		file = open(u'./tennis/templates/mail/'+ fileName+ u'.txt', u'r')
		data = u""+file.read()
		return data
	except:
		print(u"Cannot open mail template " + fileName)
		return False
		
def readBalise(data, baliseName):
	startIndex = data.find(u"<" + baliseName + u">")
	endIndex = data.find(u"<\\" + baliseName + u">", startIndex + 2 + len(baliseName))
	if startIndex == -1 or endIndex == -1:
		raise ValueError('<' + baliseName + '> balise seems to be missing in file or badly closed')
	return data[(startIndex + 2 + len(baliseName)):endIndex]

def replaceVariableBaliseByValue(data, variableName, value):
	startIndex = data.find(u"<<" + variableName + u">>")
	endIndex = startIndex + 4 + len(variableName)
	if startIndex == -1 or endIndex == -1:
		raise ValueError('<<' + variableName + '>> variable seems to be missing in file')
	return data[:startIndex] + value + data[endIndex:]

# THREAD SEND MAIL
def send_mail_sendgrid(subject, body, fromAdd, toAddList, fail_silently):
	sg = sendgrid.SendGridClient(SENDGRID_API_KEY)
	message = sendgrid.Mail()
	for mail in toAddList:
		message.add_to(mail)
	message.set_subject(subject)
	message.set_text(body)
	message.set_from(fromAdd)
	status, msg = sg.send(message)

def send_mail_via_thread(subject, message, fromAdresse, mailingList, fail_silently=False):
	if fromAdresse == "":
		fromAdresse = EMAIL_FROM
	#mailingList.append("cyril.devogelaere@student.uclouvain.be")
	try:
		threading.Thread(target=send_mail_sendgrid, args=(subject, message, fromAdresse, mailingList, fail_silently, )).start()
	except:
		print "Unexpected error in mail sending:", sys.exc_info()[0]
		return False
	return True

# MAIL CREATION
# Send a confirmation email for pair registration
def send_confirmation_email_pair_registered(participantOne, participantTwo): 
	# Init Mail variable
	playerOneFullName =  participantOne.fullName()
	playerOneAdresseMail = participantOne.user.email
	playerTwoFullName =  participantTwo.fullName()
	playerTwoAdresseMail = participantTwo.user.email
	# Read template from file
	template = u"confirm_pair_registration_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build first message from template
	try :
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		messagePlayerOne = replaceVariableBaliseByValue(message, "nameOne", playerOneFullName)
		messagePlayerOne = replaceVariableBaliseByValue(messagePlayerOne, "nameTwo", playerTwoFullName)
		messagePlayerTwo = replaceVariableBaliseByValue(message, "nameOne", playerTwoFullName)
		messagePlayerTwo = replaceVariableBaliseByValue(messagePlayerTwo, "nameTwo", playerOneFullName)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	if send_mail_via_thread(subject, messagePlayerOne, "", [playerOneAdresseMail]):
		return send_mail_via_thread(subject, messagePlayerTwo, "", [playerTwoAdresseMail])
	return False


# Send a confirmation email for court registration
def send_confirmation_email_court_registered(participant, court):
	# Init Mail variable
	fullName = participant.fullName()
	typeCourt = court.type.nom
	adresseCourt = court.getAdresse()
	disponibleSamedi = court.dispoSamedi
	disponibleDimanche = court.dispoDimanche
	mail = participant.user.email
	# Read template from file
	template = u"confirm_court_registration_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
		message = replaceVariableBaliseByValue(message, "courtAdresse", adresseCourt)
		message = replaceVariableBaliseByValue(message, "courtType", typeCourt)
		if disponibleDimanche and disponibleSamedi:
			message = replaceVariableBaliseByValue(message, "courtDisponibility", readBalise(data, "availableWeekEnd"))
		elif disponibleDimanche:
			message = replaceVariableBaliseByValue(message, "courtDisponibility", readBalise(data, "availableSunday"))
		elif disponibleSamedi:
			message = replaceVariableBaliseByValue(message, "courtDisponibility", readBalise(data, "availableSaturday"))
		else:
			message = replaceVariableBaliseByValue(message, "courtDisponibility", readBalise(data, "notAvailable"))
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])

def send_register_confirmation_email(activationObject, participant, link): 
	# Init Mail variable
	fullName = participant.fullName()
	mail = participant.user.email
	lien = link + activationObject.confirmation_key # http://domain/tennis/emailValidation/confirmation_key
	# Read template from file
	template = u"register_confirmation_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
		message = replaceVariableBaliseByValue(message, "link", lien)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])

# A tout les joueurs (excepte les iregularité de payment et les groups leader), envoyé le court sur lequels ils va jouer
def send_email_court_adress(participant, court, staff):
	# Init Mail variable
	fullName = participant.fullName()
	staffName = staff.fullName()
	mail = participant.user.email
	courtAdresse = court.getAdresse()
	# Read template from file
	template = u"court_adresse_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
		message = replaceVariableBaliseByValue(message, "courtAdresse", courtAdresse)
		message = replaceVariableBaliseByValue(message, "StaffName", staffName)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])

# Envoye a tout les player en irregularite de payment
def send_email_payment_issue(participant, extras, staff):
	# Init Mail variable
	fullName = participant.fullName()
	staffName = staff.fullName()
	montant = 20
	for extra in extras:
		montant += extra.prix
	adresseHQ = "5 Place des Carabiniers, 1030 Bruxelles"
	mail = participant.user.email
	# Read template from file
	template = u"payment_issue_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
		message = replaceVariableBaliseByValue(message, "Prix", str(montant))
		message = replaceVariableBaliseByValue(message, "Adresse", adresseHQ)
		message = replaceVariableBaliseByValue(message, "StaffName", staffName)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])

# Envoye a tout les groupes leader TODO
def send_email_score_board(participant, staff):
	# Init Mail variable
	fullName = participant.fullName()
	staffName = staff.fullName()
	adresseHQ = "5 Place des Carabiniers, 1030 Bruxelles"
	mail = participant.user.email
	# Read template from file
	template = u"group_leader_mail" 
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
		message = replaceVariableBaliseByValue(message, "Adresse", adresseHQ)
		message = replaceVariableBaliseByValue(message, "StaffName", staffName)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])
	
def send_tournament_invitation_by_mail(participant):
	# Read template from file
	template = u"tournament_invitation_mail"
	data = readTemplateFile(template)
	if data == False:
		#Can't read file
		return False
	# Init Mail variable
	fullName = participant.fullName()
	mail = participant.user.email
	# Build message from template
	try:
		subject = readBalise(data, "subject")
		message = readBalise(data, "message")
		message = replaceVariableBaliseByValue(message, "nameOne", fullName)
	except ValueError as err:
		signal_error_in_mail_template_by_mail(template, err.args)
		print("Error in template modification ", err.args)
		return False
	# Send
	return send_mail_via_thread(subject, message, "", [mail])

# BULK MAILING TOURNAMENT START
def send_tournament_invite_to_all_player():
	for participant in Participant.objects.all():
		send_tournament_invitation_by_mail(participant)

def send_tournament_invite():
	threading.Thread(target=send_tournament_invite_to_all_player, args=( )).start()
	
def choose_mail_start_tournament(pair, participant, extras, poule, staff):
	if(not pair.pay):
		# Payment issue
		send_email_payment_issue(participant, extras, staff)
	elif(participant.user == poule.leader):
		# Group leader (people with payement issue are not chosen as group leader as their participation is not guaranteed)
		send_email_score_board(participant, staff)
	else:
		#Default, send email with court adresse
		send_email_court_adress(participant, poule.court, staff)

def thread_send_email_start_tournament(staff, tournoi):
	staff = Participant.objects.filter(user=staff)[0]
	for poule in Poule.objects.filter(tournoi=tournoi):
		for pair in poule.paires.all():
			choose_mail_start_tournament(pair, Participant.objects.get(user=pair.user1), pair.extra1.all(), poule, staff)
			choose_mail_start_tournament(pair, Participant.objects.get(user=pair.user2), pair.extra2.all(), poule, staff)

def send_email_start_tournament(staff, tournoi):
	threading.Thread(target=thread_send_email_start_tournament, args=(staff, tournoi, )).start()

# CONTACT MAIL
# Envoie un mail a l'adresse de contact du site
def send_contact_mail(email, subject, message):
	return send_mail(subject, message, email, [CONTACT_EMAIL], fail_silently=False)

def signal_error_in_mail_template_by_mail(template, error):
	message = u"Le template de mail '" +  template + u"' est au moin particialement incorrect. Aucun message n'a put etre envoyé a l'utilisateur.\n\nErreur recue par le programme : " + error[0]
	return send_mail("ERROR IN MAIL TEMPLATE", message, CONTACT_EMAIL, [CONTACT_EMAIL], fail_silently=False)

# TEST MAIL
# For tests only
def test_send_mail():
	pass
	
