# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-22 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safetyapp', '0005_employee_is_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='safetyapp.Employee'),
        ),
    ]
