#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Initialisation de la base de donnée")
        os.system("python manage.py fill_etatTerrain")
        os.system("python manage.py fill_surfaceTerrain")
        os.system("python manage.py fill_typeTerrain")
        os.system("python manage.py fill_extra")
        os.system("python manage.py fill_tournoi")
        os.system("python manage.py create_admingroup")
        print("Fin de l'initialisation")