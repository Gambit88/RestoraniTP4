# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restorani', '0002_auto_20170617_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
