#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tennis.models import Participant, Tournoi, Pair, TournoiTitle, TournoiCategorie#, Extra, Court
import random
from datetime import datetime

PROB_PAIR = 0.9
PROB_HOMME = 0.5

def allowedTournaments(participant1, participant2):
    today = datetime.now()
    age1 = abs(participant1.datenaissance - today)
    age1 = age1.days / 365
    age2 = abs(participant2.datenaissance - today)
    age2 = age2.days / 365
    tournoi = ""
    jour = ""
    categorie = ""
    if (age1 >= 25 and age2 <= 15) or (age1 <= 15 and age2 >= 25):
        tournoi = "Tournoi des familles"
        jour = "Samedi"
        categorie = "Tournoi des familles"
    else:
        if participant1.titre == participant2.titre:
            if (participant2.titre == 'Mr'):
                tournoi = "Double hommes"
                jour = "Dimanche"
            else:
                tournoi = "Double femmes"
                jour = "Dimanche"
        else:
            tournoi = "Double mixte"
            jour = "Dimanche"
        
        ageMax = 0
        if age1 > age2:
            ageMax = age1
        else:
            ageMax = age2
        
        if ageMax >= 41:
            categorie = "Elites"
        elif ageMax >= 20:
            categorie = "Seniors"
        elif ageMax >= 17:
            categorie = "Juniors"
        elif ageMax >= 15:
            categorie = "Scolaires"
        elif ageMax >= 13:
            categorie = "Cadets"
        elif ageMax >= 11:
            categorie = "Minimes"
        elif ageMax >= 9:
            categorie = "Pre minimes"
    
    print(tournoi)
    t = TournoiTitle.objects.get(nom=tournoi)
    print(categorie)
    c = TournoiCategorie.objects.get(nom=categorie)
    tour = Tournoi.objects.get(titre=t, categorie=c)
    
    return tour

class Command(BaseCommand):
    def createPairs(self):
        '''
        Crée des paires à partir de deux utilisateurs qui ne sont pas déjà liés
        à une paire.
        '''
        alone_participants = list(self.Participants)
        for pair in self.Pairs:
            username1 = pair.user1.username
            username2 = pair.user2.username
            toRemove = []
            
            for participant in alone_participants:
                user = participant.user
                if username1 == user.username:
                    toRemove.append(participant)
                if username2 == user.username:
                    toRemove.append(participant)
            for e in toRemove:
                alone_participants.remove(e)
        i = 0
        while i < len(alone_participants) - 2:
            print(repr(i) + "/" + repr(len(alone_participants)))
            participant1=alone_participants[i] 
            participant2=alone_participants[i+1]
            #print(repr(participant1.user))
            #print(repr(participant2.user))
            pair = Pair(tournoi=allowedTournaments(participant1, participant2), user1=participant1.user, user2=participant2.user, valid=random.choice([True, False]), pay=random.choice([False,True]),confirm=True)
            pair.save()
            i += 2

    def handle(self, *args, **options):
        # On récupère toute la base de données
        self.Participants = Participant.objects.all()
        #self.Extras = Extra.objects.all()
        #self.Courts = Court.objects.all()
        self.Tournois = Tournoi.objects.all()
        self.Pairs = Pair.objects.all()

        self.createPairs()

