# /usr/bin/env python
# coding: utf8
'''
This program will provide you a number of people following different criteria
(women, men, age, ...) from http://en.fakenamegenerator.com
'''
import re
from selenium import webdriver
from sys import stdout

# Output file path
OUTPUT_FILE = 'res.csv'

# Total number of people to create
NBR_PEOPLE = 1

# We will open a Firefox browser...
# I set my profile because with AdBlock it is much faster
PROFILE = webdriver.FirefoxProfile(
    "/home/florian/.mozilla/firefox/mwad0hks.default")
browser = webdriver.Firefox(PROFILE)

# Some useful regular expression to parse the HTML
regex_name_start = "(.*)<h3>(.*)"
regex_name_stop = "(.*)<h3>(.*?)</h3>(.*)"
regex_addr_start = '(.*)<div class="adr">(.*)'
regex_addr_stop = "(.*)<br />(.*?)</div>(.*)"
regex_geo_start = "(.*)<dt>Geo coordinates</dt>(.*)"
regex_geo_stop = "(.*)<dd>(.*?)</dd>(.*)"
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
list_info = ["Nom", "Adresse", "Téléphone", "Date",
             "Email", "Username", "Password", "GeoData"]
list_regex_to_find = [regex_name_start, regex_addr_start, regex_phone_start, regex_birth_start,
                      regex_email_start, regex_username_start, regex_password_start, regex_geo_start]
list_regex_get = [regex_name_stop, regex_addr_stop, regex_phone_stop, regex_birth_stop,
                  regex_email_stop, regex_username_stop, regex_password_stop, regex_geo_stop]


# Dictionary of people to create :
def get_url(min_age, max_age, pourcent_men, pourcent_women):
    '''
    Returns the url needed to get the random people asked
    '''
    if min_age < 0 or max_age < 0 or min_age > max_age:
        print 'There is a problem in your choice of minimum age and maximum age'
        exit()
    if pourcent_men < 0 or pourcent_women < 0 or pourcent_men + pourcent_women != 100:
        print 'The sum of the pourcentages of men and women should be equals to 100'
        exit()
    return 'http://en.fakenamegenerator.com/advanced.php?t=country&n[]=fr&c[]=bg&gen=' + repr(pourcent_men) + '&age-min=' + repr(min_age) + '&age-max=' + repr(max_age)

def month_text_to_int(month_text):
    month_number = 0
    if month_text == "January":
        month_number = 1
    elif month_text == "February":
        month_number = 2
    elif month_text == "March":
        month_number = 3
    elif month_text == "April":
        month_number = 4
    elif month_text == "May":
        month_number = 5
    elif month_text == "June":
        month_number = 6
    elif month_text == "July":
        month_number = 7
    elif month_text == "August":
        month_number = 8
    elif month_text == "September":
        month_number = 9
    elif month_text == "October":
        month_number = 10
    elif month_text == "November":
        month_number = 11
    elif month_text == "December":
        month_number = 12
    return month_number

def parse_page(browser, url):
    '''
    Parse a page from fakenamegenerator and returns a People object that is
    partially completed
    '''
    browser.get(url)
    src = browser.page_source
    src = src.split("\n")
    ppl = People()
    for a in range(len(src)):
        i = 0
        for regex in list_regex_to_find:
            if re.match(regex, src[a]):
                if regex == regex_name_start:
                    name = re.match(list_regex_get[i], src[a]).group(2)
                    ppl.first_name = u'' + name.split()[0]
                    ppl.last_name = u'' + name.split()[1]
                elif regex == regex_email_start:
                    mail = re.match(list_regex_get[
                            i], src[a + 2]).group(2).split(' ')[0]
                    ppl.email = mail
                elif regex == regex_addr_start:
                    addr = src[a + 1]
                    addr = addr.replace("<br />", " ")
                    addr = addr.replace("  ", "")
                    addr = addr.replace("</div>", "")
                    addr = addr.split(" ")
                    i = 0
                    for ad in addr:
                        if ad.isdigit():
                            if i == 0:
                                ppl.street_number = ad
                                i += 1
                            else:
                                ppl.zipcode = ad
                        else:
                            if i == 0:
                                ppl.street += " " + ad
                            else:
                                ppl.city = ad
                elif regex == regex_geo_start:
                    geo = re.match(list_regex_get[i], src[a + 1]).group(2)
                    geo = geo.replace(
                        '<a href="javascript:void(0)" id="geo">', '')
                    geo = geo.replace('</a>', '')
                    ppl.latitude = geo.split(',')[0]
                    ppl.longitude = geo.split(',')[1]
                elif regex == regex_phone_start:
                    ppl.phone = re.match(list_regex_get[i], src[a + 1]).group(2)
                elif regex == regex_birth_start:
                    val = re.match(list_regex_get[i], src[a + 1]).group(2)
                    val = val.replace(",", "")
                    val = val.split(" ")
                    ppl.birth_day = val[1]
                    ppl.birth_month = repr(month_text_to_int(val[0]))
                    ppl.birth_year = val[2]
                elif regex == regex_username_start:
                    username = re.match(list_regex_get[
                            i], src[a + 1]).group(2)
                    ppl.username = username
                elif regex == regex_password_start:
                    password = re.match(list_regex_get[i], src[a + 1]).group(2)
                    ppl.password = password
            i += 1
    return ppl


class People(object):
    '''
    This is a model for a person.
    '''

    def __init__(self):
        self.sex = ""
        self.first_name = ""
        self.last_name = ""
        self.phone = ""
        self.street = ""
        self.street_number = ""
        self.zipcode = ""
        self.city = ""
        self.birth_day = ""
        self.birth_month = ""
        self.birth_year = ""
        self.username = ""
        self.email = ""
        self.password = ""
        self.latitude = ""
        self.longitude = ""

    def full_address(self):
        ''' Returns the complete address of the person '''
        return self.street_number + ', ' + self.street + ' ' + self.zipcode + ' ' + self.city

    def full_european_birthdate(self):
        ''' Returns the birthdate of the person as dd/mm/yyyy'''
        return self.birth_day + '/' + self.birth_month + '/' + self.birth_year

    def export_csv(self):
        ''' Returns all the fields of People separated with a comma '''
        return self.sex + u',' + self.first_name + u',' + self.last_name + u',' + \
            self.phone + u',' + self.street_number + u',' + self.street + u',' + \
            self.zipcode + u',' + self.city + u',' + self.birth_day + u',' + \
            self.birth_month + u',' + self.birth_year + u','+ self.username + \
            u',' + self.password + u',' + self.email + u',' + self.latitude + \
            u',' + self.longitude

class Generator(object):
    '''
    Class that allows you to generate with a browser a list of people following
    different criteria.
    '''
    def __init__(self, browser):
        self.browser = browser

    def generate(self, number_of_people, min_age, max_age, pourcent_men):
        '''
        Returns a list of length number_of_people containing a (pourcent_men) of
        men and a (100-pourcent_men) of women between (min_age) years old and
        (max_age) years old.
        '''
        people_list = []
        number_of_men = int(float(pourcent_men)/100 * float(number_of_people))
        number_of_women = number_of_people - number_of_men
        # Set url for 100% men
        url = get_url(min_age, max_age, 100, 0)
        for r in range(number_of_men):
            stdout.write('\rHommes:' +repr(r) + '/' + repr(number_of_men))
            stdout.flush()
            man = parse_page(self.browser, url)
            man.sex = 'Mr'
            people_list.append(man)

        # Set url for 100% women
        url = get_url(min_age, max_age, 0, 100)
        for r in range(number_of_women):
            stdout.write('\rFemmes:' +repr(r) + '/' + repr(number_of_women))
            stdout.flush()
            woman = parse_page(self.browser, url)
            woman.sex = 'Ms'
            people_list.append(woman)

        return people_list

if __name__ == '__main__':
    personnes = []
    generator = Generator(browser)
    for n in range(NBR_PEOPLE):
        stdout.write(repr(n) + '/' + repr(NBR_PEOPLE))
        stdout.flush()
        personnes += generator.generate(5000, 8, 65, 50)

    with open(OUTPUT_FILE, 'a') as output:
        for p in personnes:
            try:
                output.write(p.export_csv())
                output.write("\n")
            except UnicodeEncodeError:
                print 'UnicodeEncodeError'
    browser.close()
