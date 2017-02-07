# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20170205_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='is_instagram_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(blank=True, choices=[(b'walk', b'Walk'), (b'coffee', b'Coffee'), (b'drink', b'Drink'), (b'long_drive', b'Long Drive'), (b'lunch', b'Lunch'), (b'dinner', b'Dinner'), (b'detour', b'Detour'), (b'movie', b'Movie')], max_length=20),
        ),
    ]