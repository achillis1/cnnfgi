# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-22 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safetyapp', '0004_employee_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]