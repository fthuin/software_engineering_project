#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import CourtSurface

list_surfaces = ['Terre battue', 'Synthétique', 'Quick', 'Gazon', 'Béton', 'Brique', 'Autre']

class Command(BaseCommand):
    def addBasicSurfaces(self):
        for surface in list_surfaces:
            s = CourtSurface(nom=surface)
            s.save()

    def handle(self, *args, **options):
        self.addBasicSurfaces()

