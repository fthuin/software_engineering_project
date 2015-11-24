# -*- coding: utf-8 -*- 
from splinter import Browser      
import threading          

def validateClassementOfParticipant(participant):
	name = participant.prenom.upper() + "  " + participant.nom.upper()
	with Browser() as browser: 
		# Enter search information
		browser.visit('http://www.classement-tennis.be/calcul.html')
		if not browser.is_text_present("Recherchez un joueur en tapant son numéro d'affiliation ou son nom."):
			# Didn't load right page, close it
			# print("No Connection")
			return 
		browser.find_by_id('aft_id').fill(name)
		resultList = browser.find_by_text(name)
		if not len(resultList) == 1:
			# Multiple or no result for name, ask for staff's help as it can't be validated automatically
			# print("Multiple result")
			return
		resultList.last.click()
		# We are on the page, see if it's the correct page and if it is, return classement
		if browser.is_text_present('Classement actuel: '):
			# Correct page
			# print(browser.find_by_tag('div')[46].text)   # Print Name for debug7
			participant.classement = browser.find_by_tag('div')[48].text[len('Classement actuel: '):] # Ranking
			participant.isClassementVerified = True # Boolean for verification
			participant.save()
		else:
			# Something happened and we are back on main page, give up and unvalid it
			# print("Bad link / page changed")
			pass
	return 
	
def validate_classement_thread(participant):
	threading.Thread(target=validateClassementOfParticipant, args=(participant, )).start()