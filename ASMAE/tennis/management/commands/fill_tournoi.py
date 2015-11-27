#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import TournoiTitle, TournoiCategorie, Tournoi, TournoiStatus, PouleStatus, infoTournoi
import datetime

####################
#Titre des tournois#
####################
list_title = ['Tournoi des familles', 'Double mixte', 'Double hommes', 'Double femmes']
title_dict = dict()
for elem in list_title:
    title_dict[elem] = dict()

title_dict[list_title[0]]["description"] = "Ce tournoi organisé le samedi est destiné à un public familial, chaque paire doit contenir un enfant de moins de 15 ans et un adulte de plus de 25 ans. Les meilleurs groupes du matin pourront accéder aux éliminatoires organisés durant l'après-midi."
title_dict[list_title[0]]["jour"] = "Samedi"
title_dict[list_title[0]]["sexe1"] = None
title_dict[list_title[0]]["sexe2"] = None
title_dict[list_title[1]]["description"] = "Ce tournoi organisé le samedi est destiné à des couples ou des amis, chaque paire doit contenir un homme et une femme. Les meilleurs groupes du matin pourront accéder aux éliminatoires organisés durant l'après-midi."
title_dict[list_title[1]]["jour"] = "Samedi"
title_dict[list_title[1]]["sexe1"] = 'homme'
title_dict[list_title[1]]["sexe2"] = 'femme'
title_dict[list_title[2]]["description"] = "Ce tournoi organisé le dimanche est destiné à un public masculin uniquement. Les meilleurs groupes du matin pourront accéder aux éliminatoires organisés durant l'après-midi."
title_dict[list_title[2]]["jour"] = "Dimanche"
title_dict[list_title[2]]["sexe1"] = 'homme'
title_dict[list_title[2]]["sexe2"] = 'homme'
title_dict[list_title[3]]["description"] = "Ce tournoi organisé le dimanche est destiné à un public féminin uniquement. Les meilleurs groupes du matin pourront accéder aux éliminatoires durant l'après-midi."
title_dict[list_title[3]]["jour"] = "Dimanche"
title_dict[list_title[3]]["sexe1"] = 'femme'
title_dict[list_title[3]]["sexe2"] = 'femme'

#########################
#Catégories des tournois#
#########################
list_categorie = ['Pre minimes', 'Minimes', 'Cadets', 'Scolaires', 'Juniors', 'Seniors', 'Elites']
categorie_dict = dict()
for elem in list_categorie:
    categorie_dict[elem] = dict()

categorie_dict[list_categorie[0]]['age_min_p1'] = 9
categorie_dict[list_categorie[0]]['age_max_p1'] = 10
categorie_dict[list_categorie[0]]['age_min_p2'] = 9
categorie_dict[list_categorie[0]]['age_max_p2'] = 10

categorie_dict[list_categorie[1]]['age_min_p1'] = 11
categorie_dict[list_categorie[1]]['age_max_p1'] = 12
categorie_dict[list_categorie[1]]['age_min_p2'] = 11
categorie_dict[list_categorie[1]]['age_max_p2'] = 12

categorie_dict[list_categorie[2]]['age_min_p1'] = 13
categorie_dict[list_categorie[2]]['age_max_p1'] = 14
categorie_dict[list_categorie[2]]['age_min_p2'] = 13
categorie_dict[list_categorie[2]]['age_max_p2'] = 14

categorie_dict[list_categorie[3]]['age_min_p1'] = 15
categorie_dict[list_categorie[3]]['age_max_p1'] = 16
categorie_dict[list_categorie[3]]['age_min_p2'] = 15
categorie_dict[list_categorie[3]]['age_max_p2'] = 16

categorie_dict[list_categorie[4]]['age_min_p1'] = 17
categorie_dict[list_categorie[4]]['age_max_p1'] = 19
categorie_dict[list_categorie[4]]['age_min_p2'] = 17
categorie_dict[list_categorie[4]]['age_max_p2'] = 19

categorie_dict[list_categorie[5]]['age_min_p1'] = 20
categorie_dict[list_categorie[5]]['age_max_p1'] = 40
categorie_dict[list_categorie[5]]['age_min_p2'] = 20
categorie_dict[list_categorie[5]]['age_max_p2'] = 40

categorie_dict[list_categorie[6]]['age_min_p1'] = 41
categorie_dict[list_categorie[6]]['age_max_p1'] = 100
categorie_dict[list_categorie[6]]['age_min_p2'] = 41
categorie_dict[list_categorie[6]]['age_max_p2'] = 100

#################
#Status tournois#
#################
list_status_tournoi = ["Aucune Poules", "Poules sauvegardées", "Poules validées", "Poules terminées","Tournoi terminé"]

###############
#Status poules#
###############
list_status_poule = ["Aucun score", "En cours", "Finalisée" ]

##########
#Tournois#
##########
list_tournoi = ['Double mixte', 'Double hommes', 'Double femmes']



###########
#Commandes#
###########

class Command(BaseCommand):
    def addInfo(self):
        for elem in infoTournoi.objects.all():
            elem.delete()
        i = infoTournoi(prix=20,date=datetime.date(2016, 9, 10),addr="Place des Carabiniers, 5, 1030 Bruxelles",edition=42)
        i.save()

    def addTitle(self):
        for elem in list_title:
            descr = title_dict[elem]["description"]
            j = title_dict[elem]["jour"]
            s1 = title_dict[elem]["sexe1"]
            s2 = title_dict[elem]["sexe2"]
            t = TournoiTitle(nom=elem, description=descr, jour=j, sexe_p1=s1, sexe_p2=s2)
            t.save()

    def addCategorie(self):
        #Categorie des tournoi double mixte, femme et homme
        for elem in list_categorie:
            ami1 = categorie_dict[elem]['age_min_p1']
            ama1 = categorie_dict[elem]['age_max_p1']
            ami2 = categorie_dict[elem]['age_min_p2']
            ama2 = categorie_dict[elem]['age_max_p2']
            c = TournoiCategorie(nom=elem, age_min_p1=ami1, age_max_p1=ama1, age_min_p2=ami2, age_max_p2=ama2)
            c.save()
        #Categorie pour le tournoi des familles
        c = TournoiCategorie(nom="Tournoi des familles", age_min_p1=0, age_max_p1=15, age_min_p2=25, age_max_p2=100)
        c.save()

    def addStatusTournoi(self):
        n = 0
        for elem in list_status_tournoi:
            s = TournoiStatus(numero=n, nom=elem)
            s.save()
            n += 1
    def addStatusPoule(self):
        n = 0
        for elem in list_status_poule:
            s = PouleStatus(numero=n, nom=elem)
            s.save()
            n += 1

    
    def addTournoi(self):
        #Tournois double mixte femme et homme
        for tournoi in Tournoi.objects.all():
            tournoi.delete()
        for title in list_tournoi:
            for cat in list_categorie:
                ti = TournoiTitle.objects.get(nom = title)
                ca = TournoiCategorie.objects.get(nom = cat)
                st = TournoiStatus.objects.get(numero=0)
                t = Tournoi(titre = ti, categorie = ca, status = st)
                t.save()
        #Tournoi des familles
        ti = TournoiTitle.objects.get(nom = list_title[0])
        ca = TournoiCategorie.objects.get(nom = "Tournoi des familles")
        st = TournoiStatus.objects.get(numero=0)
        t = Tournoi(titre = ti, categorie = ca, status = st)
        t.save()

    def handle(self, *args, **options):
        print("Ajout des info du tournoi")
        self.addInfo()
        print("Ajout des titres des tournois")
        self.addTitle()
        print("Ajout des catégories des tournois")
        self.addCategorie()
        print("Ajout des status des tournois")
        self.addStatusTournoi()
        print("Ajout des status des poules")
        self.addStatusPoule()
        print("Ajout des tournois")
        self.addTournoi()