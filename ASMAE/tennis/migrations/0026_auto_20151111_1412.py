# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0025_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='court',
            name='attribue',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='court',
            field=models.OneToOneField(default=None, to='tennis.Court'),
        ),
        migrations.AlterField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, to='tennis.Groupe'),
        ),
        migrations.AddField(
            model_name='match',
            name='court',
            field=models.ForeignKey(default=None, to='tennis.Court'),
        ),
        migrations.AddField(
            model_name='match',
            name='paire_gagnante',
            field=models.ForeignKey(to='tennis.Pair', related_name='paire_gagnante'),
        ),
        migrations.AddField(
            model_name='match',
            name='paire_perdante',
            field=models.ForeignKey(to='tennis.Pair', related_name='paire_perdante'),
        ),
    ]
