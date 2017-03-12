# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 17:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tests', '0010_auto_20170310_1711'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='canswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out', models.TextField(default='')),
                ('program', models.TextField(default='')),
                ('language', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Compilerquestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prog', models.TextField(default='')),
                ('pname', models.CharField(max_length=256)),
                ('mark', models.IntegerField(default=0)),
                ('time', models.DurationField(default='0:30:00')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Apt_Test')),
            ],
        ),
        migrations.CreateModel(
            name='CompilerTestcases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcases', models.CharField(max_length=500)),
                ('test_out', models.TextField(default='No Output', max_length=1000)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncomp.Compilerquestion')),
            ],
        ),
        migrations.AddField(
            model_name='canswer',
            name='qid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncomp.Compilerquestion'),
        ),
        migrations.AddField(
            model_name='canswer',
            name='tid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Apt_Test'),
        ),
        migrations.AddField(
            model_name='canswer',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]