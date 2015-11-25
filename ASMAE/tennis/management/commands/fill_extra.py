#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tennis.models import Extra

class Command(BaseCommand):

    def handle(self, *args, **options):
        list_extra = Extra.objects.all()
        for elem in list_extra:
            elem.delete()
        print("Ajout extra barbecue")
        e = Extra(nom="Barbecue", prix=8.5, commentaires="Saucisses et hamburgers")
        e.save()