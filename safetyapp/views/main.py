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

from jeaapp.models import Customer, TradeAlly, Project, Premise, Measure, Program, CustomerDatabaseFile, Contract, ClientPO, Invoice, FiscalYear
from jeaapp.forms import MainPageFileUploadForm
from jeaapp.functions import *
from jeaapp.dependent_functions import upload_customer_database, sum_financials_and_savings


if settings.DJANGO_ENV != 'development':
    from rq import Queue
    from worker import conn

@login_required
def index(request):
    current_user = request.user
    email = current_user.email
    if 'email_address' in request.POST: email = request.POST['email_address']
    
    try:
        if request.method == 'POST':
            if 'add_customer' in request.POST:
                return HttpResponseRedirect('/customers/add/')
            elif 'customer_list' in request.POST:
                return HttpResponseRedirect('/customers/list/')
            elif 'add_trade_ally' in request.POST:
                return HttpResponseRedirect('/trade_allies/add/')
            elif 'trade_ally_list' in request.POST:
                return HttpResponseRedirect('/trade_allies/list/')
            elif 'create_report' in request.POST:
                try:
                    if settings.DJANGO_ENV != 'development':
                        w = WeeklyReport()
                        p = ProgramYear.objects.get(active = True)
                        q = Queue(connection = conn)
                        result = q.enqueue(p.create_weekly_report, w)
                    else:
                        call_command('CreateWeeklyReport', 'True') # unknown reason actual boolean True breaks; passing str instead
                    messages.success(request, 'Weekly report successfully created.')
                    return HttpResponseRedirect('/')
                except:
                    messages.error(request, 'Failed to create weekly report!')
                    return HttpResponseRedirect('/')
            elif 'load_trade_ally_list' in request.POST:
                try:
                    file_form = MainPageFileUploadForm(request.POST, request.FILES)
                    if file_form.is_valid():
                        raw_file = file_form.cleaned_data['file_field']
                        if raw_file is not None:
                            wb = load_workbook(filename=io.BytesIO(raw_file.read()))
                            ws = wb.worksheets[0]
                            fail_count = 0
                            fail_list = []
                            for row in ws.rows[1:]:
                                try:
                                    s = TradeAlly.objects.get(partner_number=row[0].value)
                                    s.company_name = row[1].value if row[1].value is not None else ''
                                    s.contact_address = row[3].value if row[3].value is not None else ''
                                    s.contact_address_2 = row[4].value if row[4].value is not None else ''
                                    s.city = row[6].value if row[6].value is not None else ''
                                    s.zipcode = row[7].value if row[7].value is not None else ''
                                    s.email = row[8].value if row[8].value is not None else ''
                                    s.company_phone = row[9].value + row[10].value + row[11].value if row[9].value is not None else ''
                                    s.commercial = True if row[12].value == 'Yes' else False
                                    s.residential = True if row[13].value == 'Yes' else False
                                    s.discipline_lighting = True if row[14].value == 'Yes' else False
                                    s.discipline_electrical = True if row[15].value == 'Yes' else False
                                    s.discipline_hvac = True if row[16].value == 'Yes' else False
                                    s.discipline_roofing = True if row[17].value == 'Yes' else False
                                    s.discipline_compressed_air = True if row[18].value == 'Yes' else False
                                    s.small_business = True if row[19].value == 'Yes' else False
                                    s.discipline_insulation = True if row[20].value == 'Yes' else False
                                    s.discipline_window_tint = True if row[21].value == 'Yes' else False
                                    s.discipline_refrigeration = True if row[22].value == 'Yes' else False
                                    s.discipline_gaskets = True if row[23].value == 'Yes' else False
                                    s.save()
                                except:
                                    try:
                                        s = TradeAlly(partner_number=row[0].value,
                                                      company_name = row[1].value if row[1].value is not None else '',
                                                      contact_address = row[3].value if row[3].value is not None else '',
                                                      contact_address_2 = row[4].value if row[4].value is not None else '',
                                                      city = row[6].value if row[6].value is not None else '',
                                                      zipcode = row[7].value if row[7].value is not None else '',
                                                      email = row[8].value if row[8].value is not None else '',
                                                      company_phone = row[9].value + row[10].value + row[11].value if row[9].value is not None else '',
                                                      commercial = True if row[12].value == 'Yes' else False,
                                                      residential = True if row[13].value == 'Yes' else False,
                                                      discipline_lighting = True if row[14].value == 'Yes' else False,
                                                      discipline_electrical = True if row[15].value == 'Yes' else False,
                                                      discipline_hvac = True if row[16].value == 'Yes' else False,
                                                      discipline_roofing = True if row[17].value == 'Yes' else False,
                                                      discipline_compressed_air = True if row[18].value == 'Yes' else False,
                                                      small_business = True if row[19].value == 'Yes' else False,
                                                      discipline_insulation = True if row[20].value == 'Yes' else False,
                                                      discipline_window_tint = True if row[21].value == 'Yes' else False,
                                                      discipline_refrigeration = True if row[22].value == 'Yes' else False,
                                                      discipline_gaskets = True if row[23].value == 'Yes' else False)
                                        s.save()
                                    except:
                                        fail_count = fail_count + 1
                                        fail_list.append(row[1].value)
                        else:
                            raise TypeError
                    messages.success(request, 'Trade Ally List successfully uploaded with %s errors (IDs = %s).' % (fail_count, fail_list))
                    return HttpResponseRedirect('/')
                except:
                    messages.error(request, 'Failed to upload Trade Ally List!')
                    return HttpResponseRedirect('/')
            elif 'load_customer_database' in request.POST:
                try:
                    if settings.DJANGO_ENV != 'development':
                        for cdbf in CustomerDatabaseFile.objects.filter(load_on_next_run = True):
                            queue = Queue(connection = conn)
                            result = queue.enqueue(upload_customer_database, cdbf)
                        messages.success(request, 'Customer database upload is in progress but may take several minutes to complete.')
                        return HttpResponseRedirect('/')
                    else:
                        for cdbf in CustomerDatabaseFile.objects.filter(load_on_next_run = True):
                            result = upload_customer_database(cdbf)
                        messages.success(request, 'Customer database uploaded!')
                        return HttpResponseRedirect('/')
                except Exception as e:
                    print(str(e))
                    messages.error(request, 'Failed to upload Customers completely!')
                    return HttpResponseRedirect('/')

        elif request.method == 'GET':            
            file_form = MainPageFileUploadForm()
            csb = Program.objects.get(name = 'C&I Small Business', active = True)
            cpr = Program.objects.get(name = 'C&I Prescriptive', active = True)
            ccu = Program.objects.get(name = 'C&I Custom', active = True)
            rhu = Program.objects.get(name = 'Residential Home Energy Upgrades', active = True)
            
            t = timezone.now().date()
            current_contract = Contract.objects.filter(active = True)[0]
            current_po_set = current_contract.clientpo_set.filter(end_date__gte = t) #admin & incentive POs are combined into single ClientPO object, covers all four progs
            current_period_set = current_contract.contractperiod_set.filter(start_date__lte = t) #is this set of all periods starting prior to today?
            current_fy_set = FiscalYear.objects.filter(start_date__lte = t, end_date__gte = t)
            current_po_invoice_set = Invoice.objects.filter(client_po__in = current_po_set)
            current_fy_project_set = Project.objects.filter(status = 'Complete',
                                                            reporting_invoice_date__range = (current_fy_set[0].start_date, current_fy_set[0].end_date))
            
            po_totals = sum_financials_and_savings(current_po_set)
            period_totals = sum_financials_and_savings(current_period_set)
            fiscal_year_totals = sum_financials_and_savings(current_fy_set)
            
            # Begin WN: given set of periods, determine oldest date and most recent date;
            # next, given set of invoices compare each Inv date to the period set date range
            # make list of Invoices that are w/in the range, use dependent fxn to sum fields by program
            # Calculate "remaining" values by subtracting actual svgs/spend from period or PO targets/budgets
            period_earliest_date = t
            period_latest_date = t
            this_period_number = 0
            for p in current_period_set:
                period_earliest_date = p.start_date if p.start_date <= period_earliest_date else period_earliest_date
                period_latest_date = p.end_date if p.end_date >= period_latest_date else period_latest_date
                this_period_number = p.period_number if p.period_number > this_period_number else this_period_number       
            period_latest_date += timedelta(1) #per django docs (field lookups), add a day so that queryset range filter will capture dates equivalent to the last day, reason: range goes from 00:00:00 to 00:00:00, not to 11:59:59; this is all probably moot since latest date will be in future but is more robust this way. I dno't understand why even if the interpretation is 00:00:00, if time is not present, the day part should still be recognized as w/in the range. No?
            all_po_set = current_contract.clientpo_set.all()
            cumulative_invoices_set = Invoice.objects.filter(client_po__in = all_po_set, invoice_date__range = (period_earliest_date, period_latest_date))   
            period_spend = {} #incentives handled in 'actuals_' block below
            period_spend = sum_financials_and_savings(cumulative_invoices_set) #the dependent function returns a two layer dictionary 
            po_spend = {}
            po_spend = sum_financials_and_savings(current_po_invoice_set)
            #End WN
            
            # actuals
            actuals_project_counts = {}
            actuals_savings_kw = {}
            actuals_savings_kwh = {}
            actuals_incentives = {}
            actuals_admin = {}
            
            # contract period targets/budgets
            period_kw = {}
            period_kwh = {}
            period_incentives = {}
            period_admin = {}
            
            # fiscal year targets/budgets
            fiscal_year_kw = {}
            fiscal_year_kwh = {}
            fiscal_year_incentives = {}
            fiscal_year_admin = {}
            
            # sum of PO budgets
            po_incentives_budget = {}
            po_admin_budget = {}
            po_admin = {}
            po_incentives = {}
            
            # sum of invoices
            invoices_incentives = {}
            invoices_admin = {}
            
            # Period and PO Balances
            period_remaining_budget = {}
            period_remaining_kwh = {}
            po_remaining_budget = {}
            
            for prog in [cpr, ccu, csb, rhu]:
                actuals_project_counts[prog.name] = Project.objects.filter(program = prog, status = 'Complete').count()
                actuals_savings_kw[prog.name] = Measure.objects.filter(project__program = prog, project__status = 'Complete').aggregate(Sum('savings_kw'))['savings_kw__sum']
                actuals_savings_kwh[prog.name] = Measure.objects.filter(project__program = prog, project__status = 'Complete').aggregate(Sum('savings_kwh'))['savings_kwh__sum']
                actuals_incentives[prog.name] = Measure.objects.filter(project__program = prog, project__status = 'Complete').aggregate(Sum('incentives'))['incentives__sum']
                actuals_admin[prog.name] = period_spend[prog.name]['administrative'] #WN added
                
                #WN fill-in single layer dictionaries with corresponding entries from two-layer dictionaries
                period_kw[prog.name] = period_totals[prog.name]['savings_kw']
                period_kwh[prog.name] = period_totals[prog.name]['savings_kwh']
                period_incentives[prog.name] = period_totals[prog.name]['incentives']
                period_admin[prog.name] = period_totals[prog.name]['administrative']
                
                fiscal_year_kw[prog.name] = fiscal_year_totals[prog.name]['savings_kw']
                fiscal_year_kwh[prog.name] = fiscal_year_totals[prog.name]['savings_kwh']
                fiscal_year_incentives[prog.name] = fiscal_year_totals[prog.name]['incentives']
                fiscal_year_admin[prog.name] = fiscal_year_totals[prog.name]['administrative']
                
                po_incentives_budget[prog.name] = po_totals[prog.name]['incentives'] #WN changed from fiscal_year_totals to po_totals
                po_admin_budget[prog.name] = po_totals[prog.name]['administrative']#WN changed from fiscal_year_totals to po_totals
                po_incentives[prog.name] = Measure.objects.filter(project__in = current_fy_project_set,
                                                                  project__program = prog,
                                                                  project__status = 'Complete').aggregate(Sum('incentives'))['incentives__sum'] #po_spend[prog.name]['incentives']#WN added
                po_incentives[prog.name] = po_incentives[prog.name] if po_incentives[prog.name] is not None else Decimal(0)
                po_admin[prog.name] = po_spend[prog.name]['administrative']#WN added
                
                #Begin WN, determine savings target and incentives budget balances at both Period and PO level
                period_remaining_budget[prog.name]= (period_admin[prog.name]+period_incentives[prog.name])-(actuals_admin[prog.name]+actuals_incentives[prog.name])
                period_remaining_kwh[prog.name]= period_kwh[prog.name]-actuals_savings_kwh[prog.name]
                po_remaining_budget[prog.name] = (po_admin_budget[prog.name]+po_incentives_budget[prog.name]) - (po_admin[prog.name] + po_incentives[prog.name])
                
            #WN redefine dictionaries to handle trivial case (presumably to print "0" instead of "None"?)
            for prog in [cpr, ccu, csb, rhu]:
                actuals_project_counts[prog.name] = actuals_project_counts[prog.name] if actuals_project_counts[prog.name] is not None else Decimal(0)
                actuals_incentives[prog.name] = actuals_incentives[prog.name] if actuals_incentives[prog.name] is not None else Decimal(0)
                actuals_savings_kw[prog.name] = actuals_savings_kw[prog.name] if actuals_savings_kw[prog.name] is not None else Decimal(0)
                actuals_savings_kwh[prog.name] = actuals_savings_kwh[prog.name] if actuals_savings_kwh[prog.name] is not None else Decimal(0)
                actuals_admin[prog.name] = actuals_admin[prog.name] if actuals_admin[prog.name] is not None else Decimal(0)
            
            cpr_insp_passed_projects = (Project.objects.filter(program = cpr, status = 'Complete')
                                                       .filter(Q(cpr_inspection_10a__in = ['Passed']) | Q(cpr_inspection_6b__in = ['Passed'])))
            cpr_insp_passed_measures = Measure.objects.filter(project__in = cpr_insp_passed_projects)
            
            cpr_pass_count = cpr_insp_passed_projects.count()
            cpr_pass_dollars = cpr_insp_passed_measures.aggregate(Sum('incentives'))['incentives__sum']
            cpr_pass_kwh = cpr_insp_passed_measures.aggregate(Sum('savings_kwh'))['savings_kwh__sum']
            
            cpr_pass_count = cpr_pass_count if cpr_pass_count is not None else Decimal(0)
            cpr_pass_dollars = cpr_pass_dollars if cpr_pass_dollars is not None else Decimal(0)
            cpr_pass_kwh = cpr_pass_kwh if cpr_pass_kwh is not None else Decimal(0)
            
            cpr_percent_pass_count = cpr_pass_count / actuals_project_counts[cpr.name] if actuals_project_counts[cpr.name] > Decimal(0) else Decimal(0)
            cpr_percent_pass_kwh = cpr_pass_dollars / actuals_incentives[cpr.name] if actuals_incentives[cpr.name] > Decimal(0) else Decimal(0)
            cpr_percent_pass_dollars = cpr_pass_kwh / actuals_savings_kwh[cpr.name] if actuals_savings_kwh[cpr.name] > Decimal(0) else Decimal(0)
            
            rhu_insp_passed_projects = (Project.objects.filter(program = rhu, status = 'Complete')
                                                       .filter(Q(rhu_home_inspection = True) | Q(rhu_phone_inspection = True)))
            rhu_insp_passed_measures = Measure.objects.filter(project__in = rhu_insp_passed_projects)

            rhu_pass_count = rhu_insp_passed_projects.count()
            rhu_pass_dollars = rhu_insp_passed_measures.aggregate(Sum('incentives'))['incentives__sum']
            rhu_pass_kwh = rhu_insp_passed_measures.aggregate(Sum('savings_kwh'))['savings_kwh__sum']
            
            rhu_pass_count = rhu_pass_count if rhu_pass_count is not None else Decimal(0)
            rhu_pass_dollars = rhu_pass_dollars if rhu_pass_dollars is not None else Decimal(0)
            rhu_pass_kwh = rhu_pass_kwh if rhu_pass_kwh is not None else Decimal(0)
            
            rhu_percent_pass_count = rhu_pass_count / actuals_project_counts[rhu.name] if actuals_project_counts[rhu.name] > Decimal(0) else Decimal(0)
            rhu_percent_pass_kwh = rhu_pass_dollars / actuals_incentives[rhu.name] if actuals_incentives[rhu.name] > Decimal(0) else Decimal(0)
            rhu_percent_pass_dollars = rhu_pass_kwh / actuals_savings_kwh[rhu.name] if actuals_savings_kwh[rhu.name] > Decimal(0) else Decimal(0)

            context = {
                'file_form':    file_form,
                'performance':  [[x.id, x.name, actuals_project_counts[x.name],
                                actuals_incentives[x.name] if actuals_incentives[x.name] is not None else Decimal(0), 
                                actuals_savings_kw[x.name] / Decimal(1000) if actuals_savings_kw[x.name] is not None else Decimal(0),
                                actuals_savings_kwh[x.name] / Decimal(1000) if actuals_savings_kw[x.name] is not None else Decimal(0),
                                actuals_incentives[x.name] / actuals_savings_kwh[x.name] if actuals_savings_kwh[x.name] > Decimal(0) else Decimal(0)]  for x in [cpr, ccu, csb, rhu]],
                'inspections':  [[cpr.id, cpr.name,
                                '{:.0f}%'.format(cpr_percent_pass_count * 100), 
                                '{:.0f}%'.format(cpr_percent_pass_kwh * 100),
                                '{:.0f}%'.format(cpr_percent_pass_dollars * 100)],
                                [rhu.id, rhu.name,
                                '{:.0f}%'.format(rhu_percent_pass_count * 100),
                                '{:.0f}%'.format(rhu_percent_pass_kwh * 100), 
                                '{:.0f}%'.format(rhu_percent_pass_dollars * 100)]],
                'period_number': this_period_number,
                'period':       [[x.id, x.name, 
                                actuals_admin[x.name] if actuals_admin[x.name] is not None else Decimal(0),
                                actuals_incentives[x.name] if actuals_incentives[x.name] is not None else Decimal(0), 
                                period_remaining_budget[x.name] if period_remaining_budget[x.name] is not None else Decimal(0),
                                actuals_savings_kwh[x.name] / Decimal(1000) if actuals_savings_kwh[x.name] is not None else Decimal(0),
                                period_remaining_kwh[x.name] / Decimal(1000) if period_remaining_kwh[x.name] is not None else Decimal(0)] for x in [cpr, ccu, csb, rhu]],
                'po':           [[x.id, x.name,
                                po_admin[x.name] if po_admin[x.name] is not None else Decimal(0), 
                                po_incentives[x.name]  if po_incentives[x.name] is not None else Decimal(0),
                                po_remaining_budget[x.name] if po_remaining_budget[x.name] is not None else Decimal(0)]
                                for x in [cpr, ccu, csb, rhu]]
            }

    except:
        context = {}
        messages.error(request, 'Unable to process request! Please try again.')
    
    template_name = 'jeaapp/general/index.html'
    return render(request, template_name, context)

