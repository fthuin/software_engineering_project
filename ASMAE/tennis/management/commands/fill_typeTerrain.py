#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import CourtType

list_types = ['Couvert', 'Ouvert']

class Command(BaseCommand):
    def addBasicTypes(self):
        for type in list_types:
            t = CourtType(nom=type)
            t.save()

    def handle(self, *args, **options):
        print("Ajout des types de terrains")
        self.addBasicTypes()