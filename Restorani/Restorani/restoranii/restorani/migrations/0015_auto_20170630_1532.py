# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restorani', '0014_auto_20170630_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratingfood',
            name='foods',
        ),
        migrations.RemoveField(
            model_name='ratingservices',
            name='employees',
        ),
        migrations.AddField(
            model_name='ratingfood',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restorani.Food'),
        ),
        migrations.AddField(
            model_name='ratingservices',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restorani.Employee'),
        ),
    ]