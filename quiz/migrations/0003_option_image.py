# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-15 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20180115_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='image',
            field=models.ImageField(blank=True, upload_to=quiz.models.option_directory_path, verbose_name='Quiz Option Image'),
        ),
    ]
