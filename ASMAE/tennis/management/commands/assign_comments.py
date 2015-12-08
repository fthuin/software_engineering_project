# /usr/bin/env python
# coding: utf8

from django.core.management.base import BaseCommand
from tennis.models import Pair
from random import randint

class Command(BaseCommand):
    def addDummyComments(self):
        paires = Pair.objects.all()
        for paire in paires:
            r = randint(0, 100)
            if r < 25:
                paire.comment1 = "Je souhaiterais faire un commentaire sur ce match"
                paire.comment2 = "Merci de ne pas me mettre sur un terrain pourri"
                paire.save()

    def handle(self, *args, **options):
        print("Ajout de commentaires")
        self.addDummyComments()
