# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restorani', '0010_auto_20170628_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.CharField(default='Now', max_length=100),
        ),
        migrations.AddField(
            model_name='reservation',
            name='rated',
            field=models.BooleanField(default=False),
        ),
    ]
