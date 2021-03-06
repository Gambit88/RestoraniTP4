# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restorani', '0009_auto_20170628_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.ManyToManyField(to='restorani.Guest')),
            ],
        ),
        migrations.AlterField(
            model_name='reservation',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restorani.Restaurant'),
        ),
        migrations.AddField(
            model_name='invitelist',
            name='reservation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='restorani.Reservation'),
        ),
    ]
