# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='standard',
            field=models.CharField(default=b'CSA', max_length=5),
        ),
    ]
