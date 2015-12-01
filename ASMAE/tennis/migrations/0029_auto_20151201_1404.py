# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0028_auto_20151201_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infotournoi',
            name='id',
        ),
        migrations.AddField(
            model_name='infotournoi',
            name='resultats',
            field=models.ManyToManyField(to='tennis.Resultat'),
        ),
        migrations.AlterField(
            model_name='infotournoi',
            name='edition',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
