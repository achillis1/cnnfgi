# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-02 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fgi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('index', models.CharField(blank=True, max_length=255)),
                ('previous_close', models.CharField(blank=True, max_length=255)),
                ('one_week_ago', models.CharField(blank=True, max_length=255)),
                ('one_month_ago', models.CharField(blank=True, max_length=255)),
                ('one_year_ago', models.CharField(blank=True, max_length=255)),
                ('week_day', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
