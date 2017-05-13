# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('image', models.ImageField(default='/media/shop/default.png', upload_to='shop/')),
                ('address', models.CharField(blank=True, max_length=120, null=True)),
                ('description', models.CharField(blank=True, max_length=120, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(default=0, max_length=55)),
                ('category_id', models.ForeignKey(db_column='CategoryData.id', on_delete=django.db.models.deletion.CASCADE, to='category.CategoryData')),
                ('city_id', models.ForeignKey(db_column='CityData.id', on_delete=django.db.models.deletion.CASCADE, to='city.CityData')),
            ],
        ),
    ]