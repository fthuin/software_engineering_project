#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tennis.models import Participant, Court, CourtSurface, CourtType, CourtState
import random

NBR_TERRAINS = 10

class Command(BaseCommand):
    def createTerrains(self):
        '''
        Crée des terrains à partir d'un participant
        '''
        nbr = 0
        while (nbr < NBR_TERRAINS):
            participant = random.choice(self.participants)
            c = Court(rue=u'' + participant.rue, numero= participant.numero, boite=participant.boite, codepostal=participant.codepostal, localite=u''+participant.localite, matiere=random.choice(self.surfaces), type=random.choice(self.types), dispoSamedi=random.choice([True, False]), dispoDimanche=random.choice([True, False]), etat=random.choice(self.etats), valide=random.choice([True, False]), user=participant.user, latitude=participant.latitude, longitude=participant.longitude)
            c.save()
            nbr += 1
            


    def handle(self, *args, **options):
        self.etats= CourtState.objects.all()
        self.surfaces = CourtSurface.objects.all()
        self.types = CourtType.objects.all()
        self.participants = Participant.objects.all()
        
        self.createTerrains()

