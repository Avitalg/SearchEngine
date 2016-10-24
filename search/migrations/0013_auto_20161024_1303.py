# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-24 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_auto_20161024_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='date',
        ),
        migrations.AddField(
            model_name='article',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]
