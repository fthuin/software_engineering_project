#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import os
from selenium import webdriver

'''
This utility was made to create fake accounts to populate the database.
'''

# Constante
TMP_FILE = "src.tmp"
RES_FILE = "res.csv"
URL_RANDOM = "http://en.fakenamegenerator.com/advanced.php?t=country&n[]=fr&c[]=bg&gen=50&age-min=8&age-max=65"
NBR_PEOPLE = 100

''' Only need to add :
    - a constant with a number which is the position in the .csv file
    - a regex for found (at the right position)
    - a regex for take the value (at the right position)
    - a default value (for security)
    - update the MAX value at the number of field
'''

PHONE = 0
MAX = 1

regex_name_start = "(.*)<h3>(.*)"
regex_name_stop = "(.*)<h3>(.*?)</h3>(.*)"
regex_addr_start = '(.*)<div class="adr">(.*)'
regex_addr_stop = "(.*)<br />(.*?)</div>(.*)"
regex_phone_start = "(.*)<dt>Phone</dt>(.*)"
regex_phone_stop = "(.*)<dd>(.*?)</dd>(.*)"
regex_birth_start = "(.*)<dt>Birthday</dt>(.*)"
regex_birth_stop = "(.*)<dd>(.*?)</dd>(.*)"
regex_email_start = "(.*)<dt>Email Address</dt>(.*)"
regex_email_stop = "(.*)<dd>(.*?)</dd>(.*)"
regex_username_start = "(.*)<dt>Username</dt>(.*)"
regex_username_stop = "(.*)<dd>(.*?)</dd>(.*)"
regex_password_start = "(.*)<dt>Password</dt>(.*)"
regex_password_stop = "(.*)<dd>(.*?)</dd>(.*)"
list_info = ["Nom", "Adresse", "Téléphone", "Date", "Email", "Username", "Password"]
list_regex_to_find = [regex_name_start, regex_addr_start, regex_phone_start, regex_birth_start, regex_email_start, regex_username_start, regex_password_start]
list_regex_get = [regex_name_stop, regex_addr_stop, regex_phone_stop, regex_birth_stop, regex_email_stop, regex_username_stop, regex_password_stop]
default = [""]

class People :

    def __init__(self) :
        self.nom = ""
        self.prenom = ""
        self.rue = ""
        self.numero = ""
        self.codepostal = ""
        self.ville = ""
        self.telephone = ""
        self.datenaissance = ""
        self.att = {}
        self.att['Adresse'] = ""

    def add(self, key, val) :
        if key == 4:
            val = val.split(" ")
            self.att[list_info[key]] = val[0].encode('UTF-8', 'ignore')
        elif key == 1:
            val = val.encode('UTF-8', 'ignore')
            val = val.split(" ")
            i = 0
            for a in val:
                if a.isdigit():
                    if i==0:
                        self.att['Numéro'] = a
                        i+=1
                    else:
                        self.att['Code'] = a
                else:
                    if i==0:
                        self.att['Adresse'] = self.att['Adresse'] + " " + a
                    else:
                        self.att['Ville'] = a
        elif key == 3:
            val = val.encode('UTF-8', 'ignore')
            val = val.replace(",", "")
            val = val.split(" ")
            month = 0
            if val[0] == "January" :
                month = 1
            elif val[0] == "February":
                month = 2
            elif val[0] == "March":
                month = 3
            elif val[0] == "April":
                month = 4
            elif val[0] == "May":
                month = 5
            elif val[0] == "June":
                month = 6
            elif val[0] == "July":
                month = 7
            elif val[0] == "August":
                month = 8
            elif val[0] == "September":
                month = 9
            elif val[0] == "October":
                month = 10
            elif val[0] == "November":
                month = 11
            elif val[0] == "December":
                month = 12
            self.att['Date'] = val[1] + "/" + repr(month) + "/" + val[2]
                
        else:
            self.att[list_info[key]] = val.encode('UTF-8', 'ignore')

    def atts(self) :
        for i in range(MAX) :
           yield self.att.get(i, default[i])

    def write(self, f) :
        f.write(', '.join(self.atts()))
        f.write('\n')
        
    def __str__(self):
        res = ""
        for item in list_info:
            if item == "Adresse":
                res += self.att['Adresse'] + ','
                res += self.att['Numéro'] + ','
                res += self.att['Code'] + ','
                res += self.att['Ville'] + ','
            else:
                res += self.att[item] + ","
        res+= "\n"
        return res

class AllPeople :

    def __init__(self) :
        self.peoples = []

    def add(self, p) :
        self.peoples.append(p)

    def write(self, path) :
        f = open(path, 'w')

        f.write(', '.join(name))
        f.write('\n')

        for p in self.peoples :
            p.write(f)
        f.close()

    def writeRandom(self, browser) :
        browser.get(URL_RANDOM )
        src = browser.page_source

        # Read one people
        f = open(TMP_FILE, 'w')
        f.write(src.encode('ascii', 'ignore'))
        f.close()

    def addRandom(self) :
        f = open(TMP_FILE, 'r')
        ple = People()

        for line in f :
            for i, (found, get) in enumerate(zip(regex_found, regex_get)):
                if re.match(found, line) :
                    ple.add(i, re.match(get, next(f)).group(2))

        f.close()
        self.add(ple)


def generatePeople(browser):
    browser.get(URL_RANDOM)
    src = browser.page_source
    src = src.split("\n")
    ppl = People()
    for a in range(len(src)):
        i=0
        for regex in list_regex_to_find:
            if re.match(regex, src[a]):
                if regex == regex_name_start:
                    ppl.add(i, re.match(list_regex_get[i], src[a]).group(2))
                elif regex == regex_email_start:
                    ppl.add(i, re.match(list_regex_get[i], src[a+2]).group(2))
                elif regex == regex_addr_start:
                    addr = src[a+1]
                    addr = addr.replace("<br />", " ")
                    addr = addr.replace("  ", "")
                    addr = addr.replace("</div>", "")
                    ppl.add(i, addr)
                else:
                    ppl.add(i, re.match(list_regex_get[i], src[a+1]).group(2))
            i+=1
    return ppl

browser = webdriver.Firefox()
personnes = []

for i in range(NBR_PEOPLE):
    personnes.append(generatePeople(browser))

with open(RES_FILE, 'w') as file:
    for ppl in personnes:
        file.write(ppl.__str__())
