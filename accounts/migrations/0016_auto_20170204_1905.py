# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-04 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20170201_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name=b'email address'),
        ),
    ]
