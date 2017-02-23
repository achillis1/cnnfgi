from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.
from safetyapp.models import Employee, SafetyCourse

@admin.register(Employee)
class EmployeeAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['user', 'supervisor', 'employee_number', 'first_name', 'last_name',
                                    'email', 'student_number', 'is_active', 'is_enabled']}),
    ]
    list_display = ('id', 'user', 'supervisor', 'employee_number', 'first_name', 'last_name',
                    'email', 'student_number', 'is_active', 'is_enabled')
    search_fields = ['id', 'supervisor', 'employee_number', 'first_name', 'last_name',
                     'email', 'student_number', 'is_active', 'is_enabled']
    list_filter = ['is_active', 'is_enabled']
    
@admin.register(SafetyCourse)
class SafetyCourseAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['course_number']}),
    ]
    list_display = ('id', 'course_number')
    search_fields = ['id', 'course_number']

