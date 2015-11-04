# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0029_auto_20151104_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='boite',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='commentaire',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='commentaireStaff',
            field=models.TextField(null=True, blank=True),
        ),
    ]
