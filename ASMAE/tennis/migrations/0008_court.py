# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0007_auto_20151021_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('rue', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10)),
                ('boite', models.CharField(max_length=10, null=True)),
                ('codepostal', models.CharField(max_length=10)),
                ('localite', models.CharField(max_length=30)),
                ('acces', models.TextField(null=True)),
                ('matiere', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('dispoSamedi', models.BooleanField(default=False)),
                ('dispoDimanche', models.BooleanField(default=False)),
                ('etat', models.CharField(max_length=30)),
                ('commentaire', models.TextField(null=True)),
            ],
        ),
    ]
