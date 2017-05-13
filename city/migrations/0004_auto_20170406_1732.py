# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0003_auto_20170406_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercitydata',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercitydata',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='register.UserData'),
        ),
    ]
