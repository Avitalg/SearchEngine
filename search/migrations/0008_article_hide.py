# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-17 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_auto_20161017_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]