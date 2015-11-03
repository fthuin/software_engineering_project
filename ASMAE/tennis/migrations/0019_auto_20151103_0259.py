# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0018_auto_20151028_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gsize', models.IntegerField(null=True)),
                ('court', models.OneToOneField(default=None, to='tennis.Court')),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='court',
        ),
        migrations.RemoveField(
            model_name='group',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='group',
            name='tournoi',
        ),
        migrations.AlterField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(default=None, to='tennis.Groupe', null=True),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AddField(
            model_name='groupe',
            name='leader',
            field=models.ForeignKey(default=None, to='tennis.Pair'),
        ),
        migrations.AddField(
            model_name='groupe',
            name='tournoi',
            field=models.ForeignKey(default=None, to='tennis.Tournoi'),
        ),
    ]
