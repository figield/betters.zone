# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-20 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20180313_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizstats',
            name='answers_duration',
            field=models.IntegerField(default=0, verbose_name='Answers time in milliseconds'),
        ),
    ]