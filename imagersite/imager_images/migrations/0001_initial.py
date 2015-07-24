# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b"What is your album's title?", max_length=128)),
                ('description', models.TextField(help_text=b'Describe your album.')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(auto_now=True)),
                ('published', models.CharField(default=b'Private', max_length=8, choices=[(b'Public', b'Public'), (b'Private', b'Private'), (b'Shared', b'Shared')])),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=b'photo_files/%Y-%m-%d')),
                ('title', models.CharField(help_text=b"What is your photo's title?", max_length=128)),
                ('description', models.TextField(help_text=b'Describe your photo.')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(auto_now=True)),
                ('published', models.CharField(default=b'Private', max_length=8, choices=[(b'Public', b'Public'), (b'Private', b'Private'), (b'Shared', b'Shared')])),
                ('user', models.ForeignKey(related_name='photos', to='imager_profile.ImagerProfile')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover_for', to='imager_images.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='albums', to='imager_images.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(related_name='albums', to='imager_profile.ImagerProfile'),
        ),
    ]
