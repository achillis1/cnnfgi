import io, pdb
from decimal import Decimal
from openpyxl import load_workbook


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
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

def check_permission(request):
    #---check that user is an admin
    safety_dashboard_admins = Group.objects.get(name = 'safety_dashboard_admins')
    if safety_dashboard_admins in request.user.groups.all():
        return True
    else:
        return False
        
@login_required
def index(request):
    current_user = request.user
    if check_permission(request) is False:
        raise PermissionDenied
    
    try:
        if Employee.objects.filter(user = current_user).count() == 1:
            employee = Employee.objects.get(user = current_user)
        else:
            employee = None
        if request.method == 'GET':            
            
            context = {
                'employee':         employee,
                'employee_list':    Employee.objects.all(),
            }
    
    except:
        context = {}
        messages.error(request, 'Unable to process request! Please try again.')
    
    template_name = 'safetyapp/admins/index.html'
    return render(request, template_name, context)

