# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-26 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20170401_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='androiddevice',
            name='application_id',
            field=models.CharField(blank=True, help_text='Opaque application identity, should be filled in for multiple key/certificate access', max_length=64, null=True, verbose_name='Application ID'),
        ),
    ]
