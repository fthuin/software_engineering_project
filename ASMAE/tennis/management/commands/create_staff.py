#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def createStaff(self):
        group = Group.objects.create(name="staff")
        group.save()

    def handle(self, *args, **options):
        print("Creation du groupe staff")
        self.createStaff()
