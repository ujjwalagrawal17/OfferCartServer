# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferBoughtData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=120, null=True)),
                ('offer_id', models.IntegerField(default=-1)),
                ('offer_code', models.CharField(blank=True, max_length=20)),
                ('price', models.IntegerField(default=-1)),
                ('avialable', models.BooleanField(default=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OfferData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('image', models.ImageField(default='/media/offer/default.png', upload_to='offer/')),
                ('price', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('validity', models.CharField(blank=True, max_length=200, null=True)),
                ('offer_code', models.CharField(blank=True, max_length=500, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopData')),
            ],
        ),
    ]
