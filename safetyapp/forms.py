import pdb

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from safety.settings import EMAIL_PROVIDER
from safetyapp.management.commands import SendEmail_Base
from safetyapp.models import Employee, SafetyCourse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, HTML, Button, Row, Field, ButtonHolder
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab, Accordion, AccordionGroup

class FileUploadForm(forms.Form):
    """Form to upload files."""
    file_field = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

class EmployeeEditForm(forms.ModelForm):
    """Form to update Employee attributes."""
    class Meta:
        model = Employee        
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_id = 'id-employee-data-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Info',
                    Field('employee_number', css_class="input-sm", wrapper_class="col-sm-4"),
                    Field('student_number', css_class="input-sm", wrapper_class="col-sm-4"),
                    Field('employee_first_name', css_class="input-sm", wrapper_class="col-sm-4"),
                    Field('employee_last_name', css_class="input-sm", wrapper_class="col-sm-4"),
                    Field('employee_email', css_class="input-sm", wrapper_class="col-sm-4"),
            )
        )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254)
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        if html_email_template_name is not None: html_email = render_to_string(html_email_template_name, context)

        SendEmail_Base.Send(to_email, subject, html_email, EMAIL_PROVIDER)
        
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_context is not None: context.update(extra_context)

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)

