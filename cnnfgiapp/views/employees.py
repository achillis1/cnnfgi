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

from cnnfgiapp.models import Employee, SafetyCourse
from cnnfgiapp.forms import FileUploadForm
from cnnfgiapp.functions import *


if settings.DJANGO_ENV != 'development':
    from rq import Queue
    from worker import conn

def check_permission(request, employee):
    #---if User is admin, doesn't matter if they're viewing their own or someone else's Employee pages
    cnnfgi_dashboard_admins = Group.objects.get(name = 'cnnfgi_dashboard_admins')
    if cnnfgi_dashboard_admins in request.user.groups.all():
        return True
    else: #---check that User and Employee go together if User is not admin
        try:
            if Employee.objects.get(user = request.user).id == employee.id: # if User is requesting their own Employee pages...
                return True
            else: # otherwise do not let a non-admin Employee access another Employee's pages
                return False
        except:
            return False

def check_admin(request):
    cnnfgi_dashboard_admins = Group.objects.get(name = 'cnnfgi_dashboard_admins')
    if cnnfgi_dashboard_admins in request.user.groups.all():
        return True
    else:
        return False

@login_required
def index(request, employee_id):
    current_user = request.user
    employee = get_object_or_404(Employee, pk=employee_id)
    if check_permission(request, employee) is False:
        raise PermissionDenied
        
    try:
        if request.method == 'GET':            
            context = {
                'employee':     employee,
                'is_admin':     check_admin(request),
            }
    
    except:
        context = {}
        messages.error(request, 'Unable to process request! Please try again.')
    
    template_name = 'cnnfgiapp/employees/index.html'
    return render(request, template_name, context)


