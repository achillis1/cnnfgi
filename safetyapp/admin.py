from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.
from safetyapp.models import Employee, SafetyCourse, Hazard, Project

@admin.register(Employee)
class EmployeeAdmin(VersionAdmin):
    fieldsets = [
        ('Employee Info', {'fields': ['user', 'supervisor', 'employee_number', 'first_name', 'last_name', 'email']}),
        ('Business Info', {'fields': ['location', 'business_unit', 'business_unit_group', 'business_unit_practice',
                                      'is_temp', 'is_project_manager', 'is_safety_dashboard_admin',
                                      'office_safety_coord', 'field_safety_coord', 'field_equip_coord',
                                      'site_sustainability_coord', 'engineering_manager'],
                           'classes': ['collapse']}),
        ('Student Info', {'fields': ['student_number', 'is_active', 'is_enabled'], 'classes': ['collapse']}),
    ]
    list_display = ('id', 'user', 'supervisor', 'employee_number', 'first_name', 'last_name',
                    'email', 'student_number', 'is_active', 'is_enabled')
    search_fields = ['id', 'supervisor', 'employee_number', 'first_name', 'last_name', 'email', 'student_number',
                     'location', 'business_unit', 'business_unit_group', 'business_unit_practice']
    list_filter = ['is_active', 'is_enabled', 'is_temp', 'is_project_manager', 'is_safety_dashboard_admin',
                   'office_safety_coord', 'field_safety_coord', 'field_equip_coord', 'site_sustainability_coord',
                   'engineering_manager']

@admin.register(SafetyCourse)
class SafetyCourseAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['course_number',
                                    'course_name',
                                    'is_active',
                                    'notes']}),
    ]
    list_display = ('id', 'course_number', 'is_active')
    search_fields = ['id', 'course_number']
    
@admin.register(Hazard)
class HazardAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['hazard_code', 'hazard_description', 'safety_courses']}),
    ]
    list_display = ('id', 'hazard_code', 'hazard_description')
    search_fields = ['id', 'hazard_code', 'hazard_description']
    list_filter = ['hazard_code']

@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    fieldsets = [
        ('General', {'fields': ['project_number', 'project_manager', 'status', 'notes']}),
        ('Tasks', {'fields': ['t00016', 't00030', 't00001', 't00021', 't00022', 't00023', 't00024', 
                              't00025', 't00011', 't00008', 't00009', 't00013', 't00014', 't00015'],
                   'classes': ['collapse']}),
        ('Facilities', {'fields': ['f00002', 'f00003', 'f00004', 'f00005', 'f00006', 'f00007', 'f00008'],
                   'classes': ['collapse']}),
        ('Systems', {'fields': ['s00008', 's00002', 's00001', 's00004', 's00007', 's00003', 's00005', 's00006'],
                   'classes': ['collapse']}),
        ('Employees', {'fields': ['employees'], 'classes': ['collapse']}),
        ('Hazards', {'fields': ['hazards'], 'classes': ['collapse']}),
    ]
    list_display = ('id', 'project_number', 'project_manager', 'status', 'notes')
    search_fields = ['id', 'project_number', 'project_manager', 'notes']
    list_filter = ['status']

