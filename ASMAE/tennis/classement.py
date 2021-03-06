# -*- coding: utf-8 -*- 
import threading    
import time
import os
from selenium import webdriver
from tennis.models import Ranking
from selenium.common.exceptions import NoSuchElementException

# This function which should run in a thread, checks if a given participant has an belgian aft ranking.
# If it has one, it's classement will be updated and set as verified.
# If it doesn't nothing will happen
def validateClassementOfParticipant(participant):
	#Init phantom js
	name = participant.prenom.upper() + " " + participant.nom.upper()
	driver = webdriver.PhantomJS("./phantomjs")
	driver.set_window_size(1120, 550) #Very important line as the phantomjs does nothing otherwise
	driver.get('http://www.classement-tennis.be/calcul.html')
	try:
		# Input name
		driver.find_element_by_id('aft_id').send_keys(name)
	except NoSuchElementException:
		# Didn't load right page, close it
		# print("No Connection")
		participant.isClassementVerified = False
		participant.save()
		driver.quit()
		return 
	# We are on the right page
	time.sleep(1) # Wait so browser doesn't go too quickly, important to let the function on the website run properly !
	result = driver.find_elements_by_xpath("//*[contains(text(), '"+name+"')]")
	if not len(result) == 1:
		# Multiple or no result for name, ask for staff's help as it can't be validated automatically
		# print("Multiple result", len(result))
		participant.isClassementVerified = False
		participant.save()
		driver.quit()
		return 
	# Click the result 
	result[0].click()
	# We should have changed page now, check if the page is correct, if it is get the classement
	if len(driver.find_elements_by_xpath("//*[contains(text(), 'Classement actuel: ')]")) == 1:
		# Correct page
		classement = driver.find_element_by_xpath("//*[contains(text(), 'Classement actuel: ')]").text[len('Classement actuel: '):] # Ranking
		for rank in Ranking.objects.all():
			if rank.nom == classement:
				# Classement matches, update in database, set as verifed
				participant.classement = rank
				participant.isClassementVerified = True # Boolean for verification
				participant.save()
				driver.quit()
				return
		# Classement doesn't match, put boolean to false and give up
		participant.isClassementVerified = False # Boolean for verification
		participant.save()
		driver.quit()
		return 
	else:
		# Something unexcpected happened and we are on a wrong page, give up and unvalid it
		# print("Bad link / page changed")
		participant.isClassementVerified = False
		participant.save()
		driver.quit()
		return 

# Launches a thread that checks the classement of a participant using the above function.
def validate_classement_thread(participant):
	threading.Thread(target=validateClassementOfParticipant, args=(participant, )).start()
