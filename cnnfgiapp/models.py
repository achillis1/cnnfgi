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

from cnnfgiapp.functions import *


class Employee(models.Model):
    """Model for Employee."""
	
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
	
	# fields
    employee_number = models.CharField(blank=True, max_length=255)
    student_number = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    location = models.CharField(blank=True, max_length=255, 
                                choices = [('Burlington, MA', 'Burlington, MA'),
                                            ('Canada', 'Canada'),
                                            ('Cary, NC', 'Cary, NC'),
                                            ('Chandler, AZ', 'Chandler, AZ'),
                                            ('Des Moines, IA', 'Des Moines, IA'),
                                            ('Hinsdale, IL', 'Hinsdale, IL'),
                                            ('India', 'India'),
                                            ('Jacksonville, FL', 'Jacksonville, FL'),
                                            ('Louisville, CO', 'Louisville, CO'),
                                            ('Madison, WI', 'Madison, WI'),
                                            ('New York', 'New York'),
                                            ('North Carolina', 'North Carolina'),
                                            ('Salt Lake City, UT', 'Salt Lake City, UT'),
                                            ('San Francisco, CA', 'San Francisco, CA'),
                                            ('San Mateo, CA', 'San Mateo, CA'),
                                            ('Telecommuter - Argentina', 'Telecommuter - Argentina'),
                                            ('Telecommuter - Arizona', 'Telecommuter - Arizona'),
                                            ('Telecommuter - California', 'Telecommuter - California'),
                                            ('Telecommuter - Canada', 'Telecommuter - Canada'),
                                            ('Telecommuter - Colorado', 'Telecommuter - Colorado'),
                                            ('Telecommuter - Georgia', 'Telecommuter - Georgia'),
                                            ('Telecommuter - Idaho', 'Telecommuter - Idaho'),
                                            ('Telecommuter - Illinois', 'Telecommuter - Illinois'),
                                            ('Telecommuter - India', 'Telecommuter - India'),
                                            ('Telecommuter - Indiana', 'Telecommuter - Indiana'),
                                            ('Telecommuter - Kentucky', 'Telecommuter - Kentucky'),
                                            ('Telecommuter - Latvia', 'Telecommuter - Latvia'),
                                            ('Telecommuter - Maine', 'Telecommuter - Maine'),
                                            ('Telecommuter - Massachusetts', 'Telecommuter - Massachusetts'),
                                            ('Telecommuter - Michigan', 'Telecommuter - Michigan'),
                                            ('Telecommuter - Mississippi', 'Telecommuter - Mississippi'),
                                            ('Telecommuter - Nevada', 'Telecommuter - Nevada'),
                                            ('Telecommuter - New Mexico', 'Telecommuter - New Mexico'),
                                            ('Telecommuter - New York', 'Telecommuter - New York'),
                                            ('Telecommuter - North Carolina', 'Telecommuter - North Carolina'),
                                            ('Telecommuter - Oregon', 'Telecommuter - Oregon'),
                                            ('Telecommuter - Pennsylvania', 'Telecommuter - Pennsylvania'),
                                            ('Telecommuter - South Carolina', 'Telecommuter - South Carolina'),
                                            ('Telecommuter - Tennessee', 'Telecommuter - Tennessee'),
                                            ('Telecommuter - Texas', 'Telecommuter - Texas'),
                                            ('Telecommuter - USAID Djibouti/Inanda', 'Telecommuter - USAID Djibouti/Inanda'),
                                            ('Telecommuter - USAID Ethiopia', 'Telecommuter - USAID Ethiopia'),
                                            ('Telecommuter - USAID Ghana', 'Telecommuter - USAID Ghana'),
                                            ('Telecommuter - USAID Kenya', 'Telecommuter - USAID Kenya'),
                                            ('Telecommuter - USAID Nigeria', 'Telecommuter - USAID Nigeria'),
                                            ('Telecommuter - USAID Pretoria', 'Telecommuter - USAID Pretoria'),
                                            ('Telecommuter - Utah', 'Telecommuter - Utah'),
                                            ('Telecommuter - Vietnam', 'Telecommuter - Vietnam'),
                                            ('Telecommuter - Virginia', 'Telecommuter - Virginia'),
                                            ('Telecommuter - Washington ', 'Telecommuter - Washington '),
                                            ('Telecommuter - Wisconsin', 'Telecommuter - Wisconsin'),
                                            ('Telecommuter - Wyoming', 'Telecommuter - Wyoming'),
                                            ('Washington, DC', 'Washington, DC'),
                                            ('White Plains, NY', 'White Plains, NY'),
                                            ])
    business_unit = models.CharField(blank=True, max_length=255,
                                     choices = [('Corporate', 'Corporate'),
                                                ('Energy & Chem Advisory', 'Energy & Chem Advisory'),
                                                ('Markets', 'Markets'),
                                                ('Software', 'Software'),
                                                ('Utility Services', 'Utility Services'),
                                                ])
    business_unit_group = models.CharField(blank=True, max_length=255,
                                           choices = [('Corporate', 'Corporate'),
                                                        ('E&CA: Commercial', 'E&CA: Commercial'),
                                                        ('E&CA: Government', 'E&CA: Government'),
                                                        ('E&CA: Nexant Thinking', 'E&CA: Nexant Thinking'),
                                                        ('Markets', 'Markets'),
                                                        ('Software: Grid Mgmt', 'Software: Grid Mgmt'),
                                                        ('Software: iEnergy', 'Software: iEnergy'),
                                                        ('Software: Revenue Manager', 'Software: Revenue Manager'),
                                                        ('UTS: Administration', 'UTS: Administration'),
                                                        ('UTS: Energy Eff Delivery', 'UTS: Energy Eff Delivery'),
                                                        ('UTS: Strategy & Planning', 'UTS: Strategy & Planning')
                                                        ])
    business_unit_practice = models.CharField(blank=True, max_length=255,
                                              choices = [('Corp: Executive', 'Corp: Executive'),
                                                        ('Corp: Finance & Acct', 'Corp: Finance & Acct'),
                                                        ('Corp: Human Resources', 'Corp: Human Resources'),
                                                        ('Corp: Info Technology', 'Corp: Info Technology'),
                                                        ('Corp: Legal & Contracts', 'Corp: Legal & Contracts'),
                                                        ('Corp: Marketing', 'Corp: Marketing'),
                                                        ('Corp: Operations', 'Corp: Operations'),
                                                        ('Corp: Sales', 'Corp: Sales'),
                                                        ('E&CA: Commercial-Americas', 'E&CA: Commercial-Americas'),
                                                        ("""E&CA: Commercial-Intern'l""", """E&CA: Commercial-Intern'l"""),
                                                        ('E&CA: Government', 'E&CA: Government'),
                                                        ('E&CA: Nexant Thinking', 'E&CA: Nexant Thinking'),
                                                        ('Markets', 'Markets'),
                                                        ('Software: Grid Mgmt-DM360', 'Software: Grid Mgmt-DM360'),
                                                        ('Software: Grid Mgmt-Prod', 'Software: Grid Mgmt-Prod'),
                                                        ('Software: iEnergy', 'Software: iEnergy'),
                                                        ('Software: Revenue Manager', 'Software: Revenue Manager'),
                                                        ('UTS: Admin-Business Dev', 'UTS: Admin-Business Dev'),
                                                        ('UTS: Admin-Business Ops', 'UTS: Admin-Business Ops'),
                                                        ('UTS: Admin-Executive', 'UTS: Admin-Executive'),
                                                        ('UTS: EED-Business Mgmt', 'UTS: EED-Business Mgmt'),
                                                        ('UTS: EED-Business Proc', 'UTS: EED-Business Proc'),
                                                        ('UTS: EED-Engineering', 'UTS: EED-Engineering'),
                                                        ('UTS: EED-I&OD', 'UTS: EED-I&OD'),
                                                        ('UTS: EED-ICS', 'UTS: EED-ICS'),
                                                        ('UTS: EED-Marketing', 'UTS: EED-Marketing'),
                                                        ('UTS: EED-TradeAlly', 'UTS: EED-TradeAlly'),
                                                        ('UTS: S&P-FSC', 'UTS: S&P-FSC'),
                                                        ('UTS: S&P-Grid Consulting', 'UTS: S&P-Grid Consulting'),
                                                        ('UTS: S&P-Planning & Eval', 'UTS: S&P-Planning & Eval'),
                                                        ])
    
    email = models.EmailField(blank=True, max_length=255)
    
    is_active = models.BooleanField(blank = True, default = False)
    is_enabled = models.BooleanField(blank = True, default = False)
    is_temp = models.BooleanField(blank = True, default = False)
    is_project_manager = models.BooleanField(blank = True, default = False)
    is_safety_dashboard_admin = models.BooleanField(blank = True, default = False)
    office_safety_coord = models.BooleanField(blank = True, default = False)
    field_safety_coord = models.BooleanField(blank = True, default = False)
    field_equip_coord = models.BooleanField(blank = True, default = False)
    site_sustainability_coord = models.BooleanField(blank = True, default = False)
    engineering_manager = models.BooleanField(blank = True, default = False)
    
    # relationships
    user = models.OneToOneField(User, related_name='employee', null=True)
    supervisor = models.ForeignKey('Employee', null=True) # doesn't use on_delete=models.CASCADE since deleting supervisor should not delete direct reports
    
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
    is_active = models.BooleanField(blank = True, default = False)
    
    def __str__(self):
        return self.course_number

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())
    
    class Meta:
        app_label = 'safetyapp'


class Hazard(models.Model):
    """Model for Hazard."""

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
	
    # general fields
    hazard_code = models.CharField(blank=True, max_length=255)
    hazard_description = models.CharField(blank=True, max_length=255)
    
    # relationships
    safety_courses = models.ManyToManyField('SafetyCourse', blank = True)
    
    def __str__(self):
        return self.hazard_code

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())
    
    class Meta:
        app_label = 'safetyapp'


class Project(models.Model):
    """Model for Project."""
    
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
	
    # general fields
    project_number = models.CharField(blank=True, max_length=255)
    notes = models.TextField(blank=True)
    status = models.CharField(blank=True, max_length=255, choices = [('Active', 'Active'), ('Inactive', 'Inactive')])
    
    # tasks
    t00016 = models.BooleanField(blank = True, default = False, verbose_name = """Take photographs""")
    t00030 = models.BooleanField(blank = True, default = False, verbose_name = """Use a portable or fixed ladder""")
    t00001 = models.BooleanField(blank = True, default = False, verbose_name = """Operate a circuit breaker""")
    t00021 = models.BooleanField(blank = True, default = False, verbose_name = """Open an electrical box/cabinet/panel (480V or less)""")
    t00022 = models.BooleanField(blank = True, default = False, verbose_name = """Open a facility's main electrical panel board (480V or less)""")
    t00023 = models.BooleanField(blank = True, default = False, verbose_name = """Measure voltage or test de-energization (480V or less)""")
    t00024 = models.BooleanField(blank = True, default = False, verbose_name = """Work with de-energized electrical equipment (480V or less)""")
    t00025 = models.BooleanField(blank = True, default = False, verbose_name = """Install or uninstall clamp-on CT (480V or less)""")
    t00011 = models.BooleanField(blank = True, default = False, verbose_name = """Work on electrical systems with multiple power sources""")
    t00008 = models.BooleanField(blank = True, default = False, verbose_name = """Internal inspection of light fixture""")
    t00009 = models.BooleanField(blank = True, default = False, verbose_name = """External inspection of light fixture""")
    t00013 = models.BooleanField(blank = True, default = False, verbose_name = """Direct install: light bulbs and non-wired loggers""")
    t00014 = models.BooleanField(blank = True, default = False, verbose_name = """Direct install: plumbing""")
    t00015 = models.BooleanField(blank = True, default = False, verbose_name = """Direct install: mizers""")
    # facilities
    f00002 = models.BooleanField(blank = True, default = False, verbose_name = """General industrial""")
    f00003 = models.BooleanField(blank = True, default = False, verbose_name = """General residential""")
    f00004 = models.BooleanField(blank = True, default = False, verbose_name = """General commercial""")
    f00005 = models.BooleanField(blank = True, default = False, verbose_name = """Refinery""")
    f00006 = models.BooleanField(blank = True, default = False, verbose_name = """Warehouse""")
    f00007 = models.BooleanField(blank = True, default = False, verbose_name = """Construction site""")
    f00008 = models.BooleanField(blank = True, default = False, verbose_name = """Outdoor work""")
    # systems
    s00008 = models.BooleanField(blank = True, default = False, verbose_name = """Electrical - Energized Work""")
    s00002 = models.BooleanField(blank = True, default = False, verbose_name = """Rooftops""")
    s00001 = models.BooleanField(blank = True, default = False, verbose_name = """Air handler units""")
    s00004 = models.BooleanField(blank = True, default = False, verbose_name = """Refrigeration compressor rooms""")
    s00007 = models.BooleanField(blank = True, default = False, verbose_name = """Mechanical rooms""")
    s00003 = models.BooleanField(blank = True, default = False, verbose_name = """Combustion gases""")
    s00005 = models.BooleanField(blank = True, default = False, verbose_name = """Compressed air""")
    s00006 = models.BooleanField(blank = True, default = False, verbose_name = """Steam systems""")
    
    # general relationships
    employees = models.ManyToManyField('Employee', blank = True)
    hazards = models.ManyToManyField('Hazard', blank = True)
    project_manager = models.ForeignKey('Employee', blank = True, null = True, related_name = 'managed_projects')
    
    def __str__(self):
        return self.project_number
    
    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())
    
    class Meta:
        app_label = 'safetyapp'

