# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncomp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canswer',
            name='language',
            field=models.CharField(choices=[('python', 'python'), ('java', 'java'), ('c_cpp', 'c++'), ('javascript', 'javascript')], default='python', max_length=2),
        ),
    ]
