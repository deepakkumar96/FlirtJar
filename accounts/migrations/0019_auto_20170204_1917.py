# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-04 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20170204_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, verbose_name=b'email address'),
        ),
    ]
