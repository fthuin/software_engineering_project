#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

group = Group.objects.create(name="Admin")
group.save()

class Command(BaseCommand):
    def createGroupAdmin(self):
        groupe = Group.objects.get(name="Admin")

        content_type = ContentType.objects.get(app_label='tennis', model='participant')
        permission = Permission.objects.get(codename="User", name="Manage User", content_type=content_type)
        groupe.permissions.add(permission)
        permission = Permission.objects.get(codename="Droit", name="Donner droit", content_type=content_type)
        groupe.permissions.add(permission)

        content_type = ContentType.objects.get(app_label='tennis', model='extra')
        permission = Permission.objects.get(codename="Extra", name="Manage Extra", content_type=content_type)
        groupe.permissions.add(permission)

        content_type = ContentType.objects.get(app_label='tennis', model='court')
        permission = Permission.objects.get(codename="Court", name="Manage Court", content_type=content_type)
        groupe.permissions.add(permission)

        content_type = ContentType.objects.get(app_label='tennis', model='tournoi')
        permission = Permission.objects.get(codename="TournoiDesFamilles", name="Manage tournoi des familles", content_type=content_type)
        groupe.permissions.add(permission)
        permission = Permission.objects.get(codename="DoubleHommes", name="Manage double hommes", content_type=content_type)
        groupe.permissions.add(permission)
        permission = Permission.objects.get(codename="DoubleFemmes", name="Manage double femmes", content_type=content_type)
        groupe.permissions.add(permission)
        permission = Permission.objects.get(codename="DoubleMixte", name="Manage double mixte", content_type=content_type)
        groupe.permissions.add(permission)

        content_type = ContentType.objects.get(app_label='tennis', model='pair')
        permission = Permission.objects.get(codename="Pair", name="Manage Pair", content_type=content_type)
        groupe.permissions.add(permission)

    def handle(self, *args, **options):
        print("Creation du groupe admin")
        self.createGroupAdmin()
