import os, io, pdb
from decimal import Decimal
from datetime import datetime, timedelta
from storages.backends.s3boto import S3BotoStorage

from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from cnnfgiapp.functions import *


class Fgi(models.Model):
    """Model for Employee."""

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

	# fields
    index = models.CharField(blank=True, max_length=255)
    previous_close = models.CharField(blank=True, max_length=255)
    one_week_ago = models.CharField(blank=True, max_length=255)
    one_month_ago = models.CharField(blank=True, max_length=255)
    one_year_ago = models.CharField(blank=True, max_length=255)
    week_day = models.IntegerField(default=0)

    def __str__(self):
        return self.index

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())

    class Meta:
        app_label = 'cnnfgiapp'

