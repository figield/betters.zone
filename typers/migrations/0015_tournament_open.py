# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typers', '0014_remove_round_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]
