# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20170331_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopdata',
            name='password',
            field=models.CharField(editable=False, help_text='Use\'[algo]$[salt]$[hexdigest]\' or usethe < ahref ="password/">change password form</a>.', max_length=128, verbose_name='password'),
        ),
    ]
