# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20170204_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_instagram_activated',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(blank=True, choices=[(b'walk', b'Walk'), (b'coffee', b'Coffee'), (b'drink', b'Drink'), (b'music', b'Music'), (b'long_drive', b'Long Drive'), (b'lunch', b'Lunch'), (b'dinner', b'Dinner')], max_length=20),
        ),
    ]