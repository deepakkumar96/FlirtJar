# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-15 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[(b'match', b'User Match'), (b'like', b'Like'), (b'crush', b'Crush or Superlike'), (b'coins', b'Coins'), (b'view', b'Profile View'), (b'fj_team', b'FlirtJar Team'), (b'gift', b'Gift')], default=b'fj_team', max_length=10),
        ),
    ]
