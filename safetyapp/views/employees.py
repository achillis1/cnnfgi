import io, pdb
from decimal import Decimal
from openpyxl import load_workbook


from django.conf import settings
from django.contrib import messages
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
def add(request):
    current_user = request.user
    email = current_user.email
    
    template_name = 'safetyapp/employees/add.html'
    return render(request, template_name, context)

@login_required
def employees_list(request):
    current_user = request.user
    email = current_user.email
    
    template_name = 'safetyapp/employees/list.html'
    return render(request, template_name, context)

@login_required
def edit(request):
    current_user = request.user
    email = current_user.email
    
    template_name = 'safetyapp/employees/edit.html'
    return render(request, template_name, context)

