import pdb
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from safety.settings import EMAIL_PROVIDER
from safetyapp.models import Project
from safetyapp.management.commands import SendEmail_Base

#python manage.py   SendEmail     email    content_id      general_param
#                 (mgt command)   (To:)    (various)         (various)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email_to')
        parser.add_argument('content_id')
        parser.add_argument('general_param', default=None)

    def handle(self, *args, **options):
        
        #capture content_id which will indicate which piece of functionality we're after
        content_id = options['content_id']
        
        #add blocks of code here that can be run by calling the right content_id
        #must include comment line indicating what additional arguments are used
        if content_id == 'CSB_scheduled_project_email':
            # call_command('SendEmail', 'dashley@nexant.com', 'CSB_scheduled_project_email', project.id)
            
            # create context data here for insertion into context dict below
            project = Project.objects.get(id = options['general_param'])
            appt_date = project.csb_appt_date.strftime('%m/%d/%Y')
            appt_time = project.csb_appt_time.strftime('%-I:%M %p')
            bill_account = project.bill_account.billaccount_number
            
            # turn html file + context variable into string for html body
            context = {'project': project,
                       'appt_date': appt_date,
                       'appt_time': appt_time,
                       'bill_account': bill_account,
                       }
            html_body = render_to_string('mail/CSB_scheduled_project_email.html', context)
            subject = 'C&I Small Business project %s scheduled for %s' % (project.project_number, appt_date)
            
        elif content_id == 'CSB_audited_project_email':
            # call_command('SendEmail', 'dashley@nexant.com', 'CSB_audited_project_email', project.id)
            
            # create context data here for insertion into context dict below
            project = Project.objects.get(id = options['general_param'])
            if project.csb_contractor_id_hvac > 0:
                csb_hvac_contractor = project.trade_ally.get(id = project.csb_contractor_id_hvac)
            else:
                csb_hvac_contractor = ''
            if project.csb_contractor_id_electrical > 0:
                csb_electrical_contractor = project.trade_ally.get(id = project.csb_contractor_id_electrical)
            else:
                csb_electrical_contractor = ''
            if project.csb_contractor_id_gasket > 0:
                csb_gasket_contractor = project.trade_ally.get(id = project.csb_contractor_id_gasket)
            else:
                csb_gasket_contractor = ''
            
            hvac_repl = 'Yes' if project.csb_hvac_replacement else ''
            hvac_tune = 'Yes' if project.csb_hvac_tuneup else ''
            lighting_upgrade = 'Yes' if project.csb_lighting_upgrade else ''
            gaskets = 'Yes' if project.csb_gaskets else ''
            kit = 'Yes' if project.csb_kit else ''
            
            # turn html file + context variable into string for html body
            context = {'project': project,
                       'csb_notes_audited':         project.csb_notes_audited,
                       'csb_hvac_contractor':       csb_hvac_contractor,
                       'csb_electrical_contractor': csb_electrical_contractor,
                       'csb_gasket_contractor':     csb_gasket_contractor,
                       'hvac_replacement':          hvac_repl,
                       'hvac_tuneup':               hvac_tune,
                       'lighting_upgrade':          lighting_upgrade,
                       'gaskets':                   gaskets,
                       'kit':                       kit,
                       }
            html_body = render_to_string('mail/CSB_audited_project_email.html', context)
            subject = 'C&I Small Business project %s audit results' % project.project_number
            
        #construct email send
        if '@' in options['email_to']: # single email address
            to = options['email_to']
            SendEmail_Base.Send(to, subject, html_body, EMAIL_PROVIDER)
        else: # name of a Group
            for person in [x.email for x in Group.objects.get(name = options['email_to']).user_set.all()]:
                to = [person]
                if settings.DJANGO_ENV != 'production': # only send emails to non-Nexant addresses if we're in production
                    if '@nexant.com' in person:
                        SendEmail_Base.Send(to, subject, html_body, EMAIL_PROVIDER)
                else:
                    SendEmail_Base.Send(to, subject, html_body, EMAIL_PROVIDER)

