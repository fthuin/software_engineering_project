# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0034_auto_20151107_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInWaitOfActivation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dayOfRegistration', models.DateTimeField()),
                ('confirmation_key', models.CharField(max_length=100)),
                ('participant', models.OneToOneField(to='tennis.Participant')),
            ],
        ),
    ]
