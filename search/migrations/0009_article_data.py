# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-22 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_article_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='data',
            field=models.CharField(default='', max_length=3000),
        ),
    ]
