# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tennis', '0017_participant_isgroupleader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('court', models.OneToOneField(to='tennis.Court')),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tournoi', models.ForeignKey(to='tennis.Tournoi')),
            ],
        ),
        migrations.AddField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(default=None, to='tennis.Group', null=True),
        ),
    ]
