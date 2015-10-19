# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='adresse',
            new_name='rue',
        ),
        migrations.AddField(
            model_name='participant',
            name='fax',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='participant',
            name='boite',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='classement',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='codepostal',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gsm',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='numero',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='participant',
            name='telephone',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
