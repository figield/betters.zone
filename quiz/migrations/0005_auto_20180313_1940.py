# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-13 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_question_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_duration',
            field=models.IntegerField(default=0, verbose_name='Answer time in milliseconds'),
        ),
    ]
