# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.IntegerField(default=0)),
            ],
        ),
    ]