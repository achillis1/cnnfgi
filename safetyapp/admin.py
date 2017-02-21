from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.
from safetyapp.models import Employee, SafetyCourse

@admin.register(Employee)
class EmployeeAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['employee_number', 'employee_first_name', 'employee_last_name']}),
    ]
    list_display = ('id', 'employee_number', 'employee_first_name', 'employee_last_name')
    search_fields = ['id', 'employee_number', 'employee_first_name', 'employee_last_name']
    
@admin.register(SafetyCourse)
class SafetyCourseAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['course_number']}),
    ]
    list_display = ('id', 'course_number')
    search_fields = ['id', 'course_number']

