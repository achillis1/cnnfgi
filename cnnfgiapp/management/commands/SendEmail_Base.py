import sendgrid, pdb
from cnnfgi.settings import EMAIL_USERNAME, EMAIL_PASSWORD

def Send(to_email,
         subject,
         html_body,
         provider,
         to_name=None,
         cc_email=None,
         bcc_email=None,
         from_email=None,
         text_body=None,
         cust_headers=None,
         att_name=None,
         att_file=None,
         sg_filter_on=False,
         sg_template_id=None,
         sg_substitutions=None,
         ):

    if provider=='sendgrid':

        #construct email and reference sendgrid template name to be used
        sg = sendgrid.SendGridClient(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        message = sendgrid.Mail()

        # add required fields to the message
        message.add_to(to_email)
        message.set_subject(subject)

        if text_body is not None:
            message.set_text(text_body)
        else:
            message.set_html(html_body)

        if from_email is not None:
            message.set_from(from_email)
        else:
            message.set_from('Nexant Safety Dashboard <cnnfgi@nexant.com>')

        # begin checking for optional fields and set them if they exist
        # initiate error message variables
        sg_template_error = ''
        sg_substitution_error = ''
        att_file_err = ''

        if to_name is not None:
            message.add_to_name(to_name)
        if cc_email is not None:
            message.add_cc(cc_email)
        if bcc_email is not None:
            message.add_bcc(bcc_email)
        if sg_filter_on:
            if sg_template_id is None:
                sg_template_error = 'You must specify a valid template'
            else:
                message.add_filter('templates', 'enable', '1')
                message.add_filter('templates', 'template_id', sg_template_id)
            if sg_substitutions is not None:
                message.add_substitution(sg_substitutions)
        if cust_headers is not None:
            message.set_headers(cust_headers)
        if att_name is not None:
            if att_file is None:
                att_file_err = 'You need to include a file to attach'
            message.add_attachment(att_name,att_file)


        status, msg = sg.send(message)
        

        return status, msg, sg_template_error, sg_substitution_error, att_file_err

    else:
        return "There was an error.  Maybe the provider was not valid."

        
