# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

WAIT_TIME = 1

class Inscription(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile("/home/florian/.mozilla/firefox/mwad0hks.default")
        self.driver = webdriver.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_inscription(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Accueil").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_css_selector("div.demo").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_link_text(u"Voir les résultats de l'année précédente").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@onclick=\"window.open('/resultat','_self')\"]").click()
        time.sleep(WAIT_TIME)
        # ERROR: Caught exception [ERROR: Unsupported command [waitForPopUp | _self | 30000]]
        driver.find_element_by_link_text(u"Résultats de l'édition 42 (2016)").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("//button[@onclick=\"window.open('/resultat','_self')\"]").click()
        time.sleep(WAIT_TIME)
        # ERROR: Caught exception [ERROR: Unsupported command [waitForPopUp | _self | 30000]]
        driver.find_element_by_css_selector("span.glyphicon.glyphicon-heart").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_link_text("Contact").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("florian.thuin@gmail.com")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("azerty")
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("Florian")
        driver.find_element_by_id("lastname").clear()
        driver.find_element_by_id("lastname").send_keys("Thuin")
        driver.find_element_by_id("firstname").clear()
        driver.find_element_by_id("firstname").send_keys("Florian")
        time.sleep(WAIT_TIME)
        Select(driver.find_element_by_id("select_jour")).select_by_visible_text("23")
        Select(driver.find_element_by_id("select_mois")).select_by_visible_text("Octobre")
        Select(driver.find_element_by_id("select_an")).select_by_visible_text("1992")
        time.sleep(WAIT_TIME)
        driver.find_element_by_id("gsm").clear()
        driver.find_element_by_id("gsm").send_keys("0497037307")
        driver.find_element_by_id("street").clear()
        driver.find_element_by_id("street").send_keys(u"Drève Maréchal Davout")
        driver.find_element_by_id("number").clear()
        driver.find_element_by_id("number").send_keys("17")
        driver.find_element_by_id("postalcode").clear()
        driver.find_element_by_id("postalcode").send_keys("1470")
        driver.find_element_by_id("locality").clear()
        driver.find_element_by_id("locality").send_keys("Genappe")
        time.sleep(WAIT_TIME)
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(WAIT_TIME*50)
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
