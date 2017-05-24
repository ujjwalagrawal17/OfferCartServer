# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20170515_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopotpdata',
            old_name='shop_name',
            new_name='shop_id',
        ),
        migrations.AddField(
            model_name='shopdata',
            name='id',
            field=models.AutoField(auto_created=True, default='1', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shopdata',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
