# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restorani', '0012_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
