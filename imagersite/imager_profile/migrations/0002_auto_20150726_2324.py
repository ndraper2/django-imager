# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera',
            field=models.CharField(help_text=b'What is the make and model of your camera?', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='photography_type',
            field=models.TextField(help_text=b'What is your favorite type of photography?', blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
