# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-02 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnnfgiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fgi',
            name='week_day',
            field=models.IntegerField(default=0),
        ),
    ]
