# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

WAIT_TIME = 1

class InscriptionTournoi(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile("/home/florian/.mozilla/firefox/mwad0hks.default")
        self.driver = webdriver.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_inscription_tournoi(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        time.sleep(WAIT_TIME)
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("Florian")
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("azerty")
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@onclick=\"location.href='/tournoi/inscriptionTournoi';\"]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//td[2]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("extra").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("remarque").clear()
        driver.find_element_by_id("remarque").send_keys("Ceci est un commentaire")
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("InscriptionButton").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_link_text("Deconnexion").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("Abires")
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("Eev4eede0h")
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_css_selector("body").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//td[4]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("extra").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("remarque").clear()
        driver.find_element_by_id("remarque").send_keys("Commentaire ><")
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("action").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_link_text("Terrains").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@onclick=\"location.href='/terrain/enregistrement';\"]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("street").clear()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("street").send_keys(u"Rue Archimède")
        driver.find_element_by_id("number").clear()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("number").send_keys("2")
        driver.find_element_by_id("postalcode").clear()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("postalcode").send_keys("1348")
        driver.find_element_by_id("locality").clear()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("locality").send_keys("Ottignies-Louvain-la-Neuve")
        driver.find_element_by_id("acces").clear()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("acces").send_keys(u"Par derrière la maison")
        time.sleep(WAIT_TIME)
        Select(driver.find_element_by_name("matiere")).select_by_visible_text("Quick")
        time.sleep(WAIT_TIME)
        Select(driver.find_element_by_name("type")).select_by_visible_text("Ouvert")
        time.sleep(WAIT_TIME)
        Select(driver.find_element_by_name("etat")).select_by_visible_text("Bon")
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("dispoSamedi").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("comment").clear()
        driver.find_element_by_id("comment").send_keys(u"Merci de ramasser vos déchets cette année")
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//td[3]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_link_text("Deconnexion").click()
        time.sleep(WAIT_TIME)
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("azerty")
        time.sleep(WAIT_TIME)
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("Florian")
        time.sleep(WAIT_TIME*5)
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(WAIT_TIME*10)
        driver.close()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
