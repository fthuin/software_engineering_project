#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import CourtState

list_etats = ['Très bon', 'Bon', 'Correct', 'Mauvais', 'Très mauvais']

class Command(BaseCommand):
    def addBasicStates(self):
        for state in list_etats:
            e = CourtState(nom=state)
            e.save()

    def handle(self, *args, **options):
        print("Ajout des etats des terrains")
        self.addBasicStates()