# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover_for', blank=True, to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(help_text=b'Describe your album.', blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='albums', to='imager_images.Photo', blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='published',
            field=models.CharField(default=b'Private', max_length=8, choices=[(b'Public', b'Public'), (b'Shared', b'Shared'), (b'Private', b'Private')]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(help_text=b'Describe your photo.', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='published',
            field=models.CharField(default=b'Private', max_length=8, choices=[(b'Public', b'Public'), (b'Shared', b'Shared'), (b'Private', b'Private')]),
        ),
    ]
