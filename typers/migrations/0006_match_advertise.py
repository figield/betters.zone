# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typers', '0005_friendship_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='advertise',
            field=models.BooleanField(default=False),
        ),
    ]
