# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0009_auto_20170406_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydata',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
