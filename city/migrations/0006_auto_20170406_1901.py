# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0005_auto_20170406_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercitydata',
            name='user_id',
            field=models.ForeignKey(db_column='UserData.mobile', on_delete=django.db.models.deletion.CASCADE, to='register.UserData', unique=True),
        ),
    ]
