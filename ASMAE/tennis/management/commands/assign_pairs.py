#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tennis.models import Extra, Participant, Court, Tournoi, Groupe, Pair
from random import random
from datetime import datetime

TOURNAMENT_LIST = ['Tournoi des familles', 'Double mixte', 'Double hommes', 'Double femmes']

PROB_PAIR = 0.9
PROB_HOMME = 0.5

def getRandomElementFromList(list):
    res = random()*len(list)
    return list[int(res)]
    
def allowedTournaments(participant1, participant2):
    today = datetime.now()
    age1 = abs(participant1.datenaissance - today)
    age1 = age1.days / 365
    age2 = abs(participant2.datenaissance - today)
    age2 = age2.days / 365
    resList = list(TOURNAMENT_LIST)
    if ((age1 > 15 and age1 < 25) or (age2 > 15 and age2 < 25)):
        resList.remove('Tournoi des familles')
    if (participant1.titre == 'Mr'):
        resList.remove('Double femmes')
        if (participant2.titre == 'Mme'):
            resList.remove('Double hommes')
        else:
            resList.remove('Double mixte')
    else:
        resList.remove('Double hommes')
        if (participant2.titre == 'Mme'):
            resList.remove('Double mixte')
        else:
            resList.remove('Double femmes')
    return resList

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
            for participant in alone_participants:
                user = participant.user
                if username1 == user.username:
                    alone_participants.remove(participant)
                if username2 == user.username:
                    alone_participants.remove(participant)
        i = 0
        while i < len(alone_participants) - 2:
            participant1=alone_participants[i]
            participant2=alone_participants[i+1]
            tournoi = getRandomElementFromList(allowedTournaments(participant1, participant2))
            for tour in self.Tournois:
                if tournoi == tour.nom:
                    tournoi = tour
                    break
            print(repr(tournoi))
            print(repr(participant1.user))
            print(repr(participant2.user))
            pair = Pair(tournoi=tournoi, user1=participant1.user, user2=participant2.user, confirm=True)
            pair.save()
            i += 2

    def handle(self, *args, **options):
        # On récupère toute la base de données
        self.Participants = Participant.objects.all()
        self.Extras = Extra.objects.all()
        self.Courts = Court.objects.all()
        self.Tournois = Tournoi.objects.all()
        self.Groupes = Groupe.objects.all()
        self.Pairs = Pair.objects.all()

        self.createPairs()

