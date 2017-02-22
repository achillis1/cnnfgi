import os, io, pdb
from decimal import Decimal
from datetime import datetime, timedelta
from storages.backends.s3boto import S3BotoStorage

from openpyxl import load_workbook

from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from safetyapp.functions import *


class Employee(models.Model):
    """Model for Employee."""
	
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
	
	# fields
    employee_number = models.CharField(blank=True, max_length=255)
    student_number = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    email = models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(blank = True, default = False)
    is_enabled = models.BooleanField(blank = True, default = False)
    
    # relationships
    user = models.OneToOneField(User, related_name='employee', null=True)
    
    def __str__(self):
        if self.first_name is not None and self.last_name is not None:
            return self.last_name + ', ' + self.first_name + ' (' + self.employee_number + ')'
        else:
            return self.employee_number
        
    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())

    class Meta:
        app_label = 'safetyapp'


class SafetyCourse(models.Model):
    """Model for SafetyCourse."""

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
	
    # general fields
    course_number = models.CharField(blank=True, max_length=255)
    course_name = models.CharField(blank=True, max_length=255)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.course_number

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())
    
    class Meta:
        app_label = 'safetyapp'

