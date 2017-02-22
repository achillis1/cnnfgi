import io, pdb
from decimal import Decimal
from openpyxl import load_workbook


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from safetyapp.models import Employee, SafetyCourse
from safetyapp.forms import FileUploadForm
from safetyapp.functions import *


if settings.DJANGO_ENV != 'development':
    from rq import Queue
    from worker import conn

@login_required
def index(request):
    current_user = request.user
    try:
        safety_dashboard_admins = Group.objects.get(name = 'safety_dashboard_admins')
        if Employee.objects.filter(user = current_user).count() == 1:
            employee = Employee.objects.get(user = current_user)
            return HttpResponseRedirect('/employees/%s/' % employee.id)
        elif safety_dashboard_admins in current_user.groups.all():
            return HttpResponseRedirect('/admin_index/')
        else:
            messages.error(request, """It appears you're neither an employee nor a system administrator!""")
            template_name = 'safetyapp/dead_end.html'
            return render(request, template_name, {})
    except:
        messages.error(request, 'Unable to direct your request to the right place!')
        template_name = 'safetyapp/dead_end.html'
        return render(request, template_name, {})

