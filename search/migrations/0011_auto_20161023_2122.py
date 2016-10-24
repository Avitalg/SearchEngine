# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-23 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0010_auto_20161022_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.URLField(default='www.example.com', max_length=1000),
        ),
        migrations.AlterField(
            model_name='article',
            name='data',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]
