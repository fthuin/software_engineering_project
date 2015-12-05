#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import Ranking
import datetime

###########
#Commandes#
###########

list_rankings = ["NC", "C30.5", "C30.4", "C30.3", "C30.2", "C30.1", "C30", "C15.5", "C15.4", "C15.3", "C15.2", "C15.1", "C15", "B+4/6", "B+2/6", "B0"]

class Command(BaseCommand):
    def addRankings(self):
        for elem in list_rankings:
            r = Ranking(nom=elem)
            r.save()

    def handle(self, *args, **options):
        self.addRankings()
