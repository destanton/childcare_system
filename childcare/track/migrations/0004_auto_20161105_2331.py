# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 23:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_auto_20161105_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='time',
            options={'ordering': ('-id',)},
        ),
    ]
