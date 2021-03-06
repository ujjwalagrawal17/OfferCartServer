# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_merge_20170515_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopOtpData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField(default=0, null=True)),
                ('flag', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='shopdata',
            name='active',
        ),
        migrations.AlterField(
            model_name='shopdata',
            name='name',
            field=models.CharField(default='a', max_length=255, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shopdata',
            name='password',
            field=models.CharField(default=0, max_length=55),
        ),
        migrations.AddField(
            model_name='shopotpdata',
            name='shop_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopData'),
        ),
    ]
