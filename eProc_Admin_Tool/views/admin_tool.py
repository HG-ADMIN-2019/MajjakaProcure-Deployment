"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    admin_tool.py
Usage:
   Renders admin tool page
Author:
    Varsha
"""

# Function to display home page of shopping cart app
import csv
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymysql import NULL

from eProc_Basic.Utilities.constants.constants import CONST_DATE_FORMAT, CONST_DECIMAL_NOTATION
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id, getClients, get_user_id_by_email_id
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str
from eProc_Basic_Settings.views import JsonParser_obj
from eProc_Configuration.models import *
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Emails.models import EmailUserMonitoring
from eProc_Org_Model.Utilities import client
from eProc_Org_Model.models import OrgModel
from eProc_Org_Support.models import OrgAnnouncements
from eProc_Org_Support.views import org_announcement_search
from eProc_Registration.models import UserData
from eProc_Reports.Report_Forms.SearchDoc_forms import DocumentSearchForm, ApplicationMonitoringForm, \
    EmailUserMonitoringForm
from eProc_Reports.Report_Forms.user_report_form import UserReportForm
from eProc_Reports.Utilities.reports_generic import get_companylist, get_usrid_by_username, get_account_assignlist, \
    get_langlist, get_companyDetails, get_account_assignvalues
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader, ScItem
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search
from eProc_Suppliers.Utilities.supplier_specific import get_supplier_data, update_country_encrypt
from eProc_Suppliers.models import OrgSuppliers
from eProc_Users.Utilities.user_generic import user_detail_search
from django.http import QueryDict

django_query_instance = DjangoQueries()


@login_required
def admin_tool(req):
    """
    :param req:
    :return:
    """
    context = {
        'inc_nav': True,
        'inc_footer': True,
    }
    return render(req, 'Admin_Tool/admin_tool_nav.html', context)


def user_search(request):
    update_user_info(request)
    dropdown_usertype_values = list(
        FieldTypeDesc.objects.filter(field_name='user_type', del_ind=False).values('field_type_id',
                                                                                   'field_type_desc'
                                                                                   ))
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'get_country_id': get_country_id(),
        'is_admin_active': True,
        'dropdown_usertype_values': dropdown_usertype_values,
    }

    if request.method == 'GET':
        encrypted_email = []

        employee_results = django_query_instance.django_filter_only_query(UserData, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })
        for emails in employee_results:
            encrypted_email.append(encrypt(emails.email))

        context['employee_results'] = zip(employee_results, encrypted_email)

    if request.method == 'POST':
        encrypted_email = []
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'user_locked':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if data == 'pwd_locked':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if data == 'is_active':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if value != '':
                    search_fields[data] = value

        search_fields['username'] = request.POST.get('username')
        search_fields['first_name'] = request.POST.get('first_name')
        search_fields['last_name'] = request.POST.get('last_name')
        search_fields['email'] = request.POST.get('email')
        search_fields['user_type'] = request.POST.get('user_type')
        search_fields['employee_id'] = request.POST.get('employee_id')

        employee_results = user_detail_search(**search_fields)

        for user_email in employee_results:
            encrypted_email.append(encrypt(user_email['email']))

        print(employee_results)
        context['employee_results'] = zip(employee_results, encrypted_email)

    return render(request, 'User Search/user_search.html', context)


def supplier_search(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    country_dictionary_list = django_query_instance.django_filter_query(Country,
                                                                        None, None, ['country_code', 'country_name'])
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'get_country_id': country_dictionary_list,
        'is_admin_active': True
    }

    if request.method == 'GET':
        supplier_id_encrypted = []
        supplier_results = get_supplier_data()

        context['supplier_results'] = supplier_results

    if request.method == 'POST':
        supplier_id_encrypted = []
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'block':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if value != '':
                    search_fields[data] = value

        # search_fields['client'] = client
        # search_fields['del_ind'] = False
        search_fields['name1'] = request.POST.get('name1')
        search_fields['name2'] = request.POST.get('name2')
        search_fields['supplier_id'] = request.POST.get('supplier_id')
        search_fields['search_term1'] = request.POST.get('search_term1')
        search_fields['search_term2'] = request.POST.get('search_term2')
        search_fields['country_code'] = request.POST.get('country_code')
        search_fields['city'] = request.POST.get('city')
        search_fields['block'] = request.POST.get('block')

        supplier_results = supplier_detail_search(**search_fields)
        print("supplier_results", supplier_results)
        context['supplier_results'] = update_country_encrypt(supplier_results)

    return render(request, 'Supplier Search/supplier_search.html', context)


@login_required
def user_details(request, email):
    """
    Gets the user details and render it in the user details page
    :param request: Form Request
    :param email: Email id (login id)
    :return: User details page
    """
    email = decrypt(email)
    update_user_info(request)
    date_format_array = CONST_DATE_FORMAT
    decimal_array = CONST_DECIMAL_NOTATION

    user_info = django_query_instance.django_get_query(UserData,
                                                       {'email': email, 'client': getClients(request),
                                                        'del_ind': False})

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'user_info': user_info,
        'currency_id': django_query_instance.django_filter_value_list_query(Currency, {'del_ind': False},
                                                                            'currency_id'),
        'time_zones': django_query_instance.django_filter_value_list_query(TimeZone, {'del_ind': False}, 'time_zone'),
        'language_list': django_query_instance.django_filter_value_list_query(Languages, {'del_ind': False},
                                                                              'language_id'),
        'decimal_list': decimal_array,
        'date_format_list': date_format_array,
    }

    return render(request, 'Display Edit User/display_edit_user.html', context)


@login_required
def sup_details(req, supplier_id):
    """
    Gets the selected supplier details and render it in the supplier details pop-up page
    :param supplier_id:
    :param req: Form Request
    :return: Supplier details pop-up page
    """
    if supplier_id != 'None':
        supplier_action = 'UPDATE'
        supplier_id = decrypt(supplier_id)
    else:
        supplier_action = 'CREATE'
    update_user_info(req)
    supplier_info = django_query_instance.django_get_query(SupplierMaster, {'supplier_id': supplier_id,
                                                                            'client': global_variables.GLOBAL_CLIENT})

    supplier_org_info = django_query_instance.django_filter_only_query(OrgSuppliers, {'supplier_id': supplier_id,
                                                                                      'client': getClients(req),
                                                                                      'del_ind': False})

    django_query_instance.django_filter_value_list_query(Languages, {'del_ind': False}, 'language_id')

    supp_img_info = django_query_instance.django_filter_only_query(ImagesUpload, {
        'image_id': supplier_id, 'client': getClients(req), 'del_ind': False})
    # print(supp_img_info)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'supplier_action': supplier_action,
        'supplier_info': supplier_info,
        'supplier_org_info': supplier_org_info,
        'purch_org_list': django_query_instance.django_filter_value_list_query(OrgPorg, {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False}, 'porg_id'),

        'currency_id': django_query_instance.django_filter_value_list_query(Currency, {'del_ind': False},
                                                                            'currency_id'),
        'payterm_list': django_query_instance.django_filter_value_list_query(Payterms, {
            'client': global_variables.GLOBAL_CLIENT,
            'del_ind': False}, 'payment_term_key'),

        'incoterm_list': django_query_instance.django_filter_value_list_query(Incoterms, {'del_ind': False},
                                                                              'incoterm_key'),
        'country_list': django_query_instance.django_filter_value_list_query(Country, {'del_ind': False},
                                                                             'country_code'),
        'language_list': django_query_instance.django_filter_value_list_query(Languages, {'del_ind': False},
                                                                              'language_id'),
        'supp_img_info': supp_img_info
    }

    return render(req, 'Display Edit Supplier/display_edit_supplier.html', context)


@login_required
def user_report(request):
    """
        :param request:
        :return:
        """
    user_rep_form = UserReportForm()
    final_list = []
    client = getClients(request)
    page_range = 0
    company_list = get_companylist(request)

    if not request.method == 'POST':
        if 'final_list' in request.session:
            request.POST = request.session['final_list']
            request.method = 'POST'

    if request.method == 'POST':
        request.session['final_list'] = request.POST

    # If method is post get the form values and get header details accordingly
    if request.method == 'POST':
        user_rep_form = UserReportForm(request.POST)

        if user_rep_form.is_valid():
            inp_comp_code = request.POST.get('company_code')
            inp_username = request.POST.get('username')
            inp_active = request.POST.get('active')

            if inp_active == 'Active':
                active = True
            else:
                active = False

            if inp_username is not None and inp_username != '':
                username = inp_username

                user_list_star = get_usrid_by_username(username, active)

                for list in user_list_star:
                    print("* in user name list", list.username)
                    print(list.email)
            else:
                user_list_star = django_query_instance.django_filter_only_query(UserData, {'is_active': active})
                print(user_list_star)
            ####################################################################################

            if inp_comp_code is not None:
                # UserData
                company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=inp_comp_code)

                # Using the company code number and CCODE node type get the company details from Org Model table
                for comp_det in company_details:
                    print(comp_det.company_id)

                    comp_obj_id_info = OrgModel.objects.filter(Q(object_id=comp_det.object_id_id, node_type='CCODE',
                                                                 client=client, del_ind=False))

                    ###################################################################
                    if inp_username is not None and inp_username != '':

                        for user_info in user_list_star:
                            confirm_in_comp = OrgModel.objects.filter(
                                Q(node_type='USER', name=user_info.username,
                                  client=client, del_ind=False))
                            final_array = []
                            if confirm_in_comp:
                                final_array.append(comp_det.company_id)
                                final_array.append(concatenate_str(comp_det.name1, comp_det.name2))
                                final_array.append(user_info.username)
                                final_array.append(user_info.last_name)
                                final_array.append(user_info.first_name)
                                final_array.append(user_info.email)

                                final_array.append(user_info.user_locked)

                                final_list.append(final_array)
                    else:

                        # Using the Company Details - node_guid read the NODE type which has company code node_guid
                        # as parent_node from the Org Model table
                        for comp in comp_obj_id_info:
                            node_info = OrgModel.objects.filter(Q(parent_node_guid=comp.node_guid, node_type='NODE',
                                                                  client=client, del_ind=False))

                            # Using the node info guid read all the users that have parent_node as the node guid.
                            for node in node_info:
                                user_list = OrgModel.objects.filter(Q(parent_node_guid=node.node_guid, node_type='USER',
                                                                      client=client, del_ind=False))

                                # Using the user_list from the Org Model read the user details
                                for user_obj_id in user_list:
                                    print("user_obj_id.object_id", user_obj_id.object_id)

                                    if inp_active == 'on':
                                        active = True
                                    else:
                                        active = False

                                    user_details = UserData.objects.filter(
                                        Q(object_id=user_obj_id.object_id, is_active=active,
                                          client=client, del_ind=False))

                                    final_array = []

                                    for user in user_details:
                                        print('User in Company:', user.first_name, user.username)
                                        final_array.append(comp_det.company_id)
                                        final_array.append(concatenate_str(comp_det.name1, comp_det.name2))
                                        final_array.append(user.username)
                                        final_array.append(user.last_name)
                                        final_array.append(user.first_name)
                                        final_array.append(user.email)
                                        final_array.append(user.user_locked)
                                        final_list.append(final_array)
        else:
            print(user_rep_form.errors)

    # Company code, Company name, Username, Last name, First name, Email address, Ship to address, user lock status
    user_rep_form = UserReportForm()
    t_count = len(final_list)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'user_rep_form': user_rep_form,
        'final_list': final_list,
        'page_range': page_range,
        't_count': t_count,
        'company_list': company_list,
        'is_slide_menu': True,
        'is_admin_active': True
    }

    return render(request, 'Reports/user_report.html', context)


@login_required
def approval_report(request):
    """
        :param request:
        :return:
        """

    global workflow_acc_list
    client = getClients(request)
    page_range = 0
    final_list = []

    company_array = get_companyDetails(request)
    acc_value_array = get_account_assignvalues(request)
    # for val in acc_value_array:
    acct_values = get_account_assignlist(request)
    # print(company_array[0])

    if request.method == 'GET':
        inp_comp_code = company_array[0]
        inp_acc_assgn_cat = acct_values[0]
        workflow_schema = list(WorkflowSchema.objects.filter(Q(client=client,
                                                               company_id=inp_comp_code)).values_list('app_types',
                                                                                                      flat=True))
        if workflow_schema:
            for schema_step_type in workflow_schema:
                # MMD_WF_ACC check this table model and read the data from here
                workflow_acc_list = WorkflowACC.objects.filter(Q(account_assign_cat=inp_acc_assgn_cat,
                                                                 company_id=inp_comp_code, client=client))

    if not request.method == 'POST':
        if 'final_list' in request.session:
            request.POST = request.session['final_list']
            # request.method = 'POST'

    if request.method == 'POST':
        request.session['final_list'] = request.POST
        inp_acc_assgn_cat = request.POST.getlist('acc_assgn_cat', default=None)
        inp_comp_code = request.POST.get('comp_code_app')

        if inp_comp_code is not None and inp_acc_assgn_cat is not None:
            workflow_schema = list(WorkflowSchema.objects.filter(Q(client=client,
                                                                   company_id=inp_comp_code)).values_list('app_types',
                                                                                                          flat=True))
            if workflow_schema:
                for schema_step_type in workflow_schema:
                    # MMD_WF_ACC check this table model and read the data from here
                    workflow_acc_list = WorkflowACC.objects.filter(Q(account_assign_cat__in=inp_acc_assgn_cat,
                                                                     company_id=inp_comp_code, client=client))

    if workflow_acc_list:
        for w_acc_list in workflow_acc_list:

            app_code_id = ApproverLimit.objects.filter(Q(company_id=inp_comp_code,
                                                         approver_username=w_acc_list.app_username,
                                                         del_ind=False,
                                                         client=client)).values_list('app_code_id',
                                                                                     flat=True)

            if app_code_id:
                app_val_list = ApproverLimitValue.objects.filter(Q(company_id=inp_comp_code,
                                                                   app_code_id__in=app_code_id,
                                                                   del_ind=False,
                                                                   app_types=schema_step_type,
                                                                   client=client))
                final_array = []
                for app_val in app_val_list:
                    final_array.append(w_acc_list.company_id)
                    final_array.append(w_acc_list.account_assign_cat_id)
                    final_array.append(w_acc_list.acc_value)
                    final_array.append(w_acc_list.app_username)
                    final_array.append(w_acc_list.currency_id)
                    final_array.append(w_acc_list.sup_company_id)
                    final_array.append(w_acc_list.sup_acc_value)
                    final_array.append(app_val.upper_limit_value)
                    final_array.append(app_val.currency_id)
                    final_array.append(app_val.app_code_id)
                    final_array.append(w_acc_list.sup_account_assign_cat_id)
                    final_array.append(app_val.app_code_id)
                    final_list.append(final_array)

    t_count = len(final_list)

    # Paginating search results and restricting the results to 5 per page
    # page = request.GET.get('page', 1)
    # paginator = Paginator(final_list, 5)
    # try:
    #     final_list = paginator.page(page)
    # except PageNotAnInteger:
    #     final_list = paginator.page(1)
    # except EmptyPage:
    #     final_list = paginator.page(paginator.num_pages)

    # Context to display in Doc_report.html
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'comp_list': company_array,
        'acct_val_list': acc_value_array,
        'final_list': final_list,
        'page_range': page_range,
        't_count': t_count,
        'inp_acc_assgn_cat': inp_acc_assgn_cat,
        'inp_comp_code': inp_comp_code,
        'is_slide_menu': True,
        'is_admin_active': True
    }

    return render(request, 'Reports/approval_report.html', context)


@login_required
def m_docsearch_meth(request):
    """
    :param request:
    :return:
    """
    inp_doc_type = ''
    result = ''
    page_range = 0
    report_search = False
    client = getClients(request)
    sc_header = []
    sc_appr = []
    sc_completion = []
    encrypted_header_guid = []
    sc_completion_flag = False
    page_type_flag = 'Doc_reports'
    rep_search_form = {}
    error_messages = ''
    # company code list- client n del indicator
    # users in selected company - client n del indicator
    comp_list = get_companylist(request)

    if request.method == 'GET':
        # inp_comp_code = request.GET('company_code')
        inp_doc_type = 'SC'
        inp_doc_num = None
        inp_from_date = datetime.today()
        inp_to_date = datetime.today()
        inp_supl = None
        inp_created_by = ''
        inp_requester = ''

        # result
        result = get_hdr_data(request,
                              inp_doc_type,
                              inp_doc_num,
                              inp_from_date,
                              inp_to_date,
                              inp_supl,
                              inp_created_by,
                              inp_requester, report_search)

        company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=1000)
        for comp in company_details:
            result = result.filter(co_code=comp.company_id)

    if not request.method == 'POST':
        if 'results' in request.session:
            request.POST = request.session['results']
            request.method = 'POST'

    if request.method == 'POST':
        request.session['results'] = request.POST

    # rep_search_form = DocumentSearchForm()
    # If method is post get the form values and get header details accordingly
    if request.method == 'POST':
        rep_search_form = DocumentSearchForm(request.POST)

        if rep_search_form.is_valid():
            inp_comp_code = request.POST.get('company_code')
            inp_doc_type = request.POST.get('doc_type')
            inp_doc_num = request.POST.get('doc_num')
            inp_from_date = request.POST.get('from_date')
            inp_to_date = request.POST.get('to_date')
            inp_supl = request.POST.get('supplier')
            inp_created_by = request.POST.get('created_by')
            inp_requester = request.POST.get('requester')

            # results
            result = get_hdr_data(request,
                                  inp_doc_type,
                                  inp_doc_num,
                                  inp_from_date,
                                  inp_to_date,
                                  inp_supl,
                                  inp_created_by,
                                  inp_requester, report_search)
            company_details = OrgCompanies.objects.filter(client=client, del_ind=False, company_guid=inp_comp_code)
            for comp in company_details:
                result = result.filter(co_code=comp.company_id)
    else:
        rep_search_form = DocumentSearchForm()

    error_messages = rep_search_form.errors
    t_count = len(result)

    for header_guid in result:
        encrypted_header_guid.append(encrypt(header_guid))

    # print(result)
    result = zip(result, encrypted_header_guid)

    # Context to display in Doc_report.html
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'nav_title': 'Search for document',
        'sform': rep_search_form,
        'results': result,
        'page_range': page_range,
        't_count': t_count,
        'inp_doc_type': inp_doc_type,
        'comp_list': comp_list,
        'is_slide_menu': True,
        'is_admin_active': True,
        'encrypted_header_guid': encrypted_header_guid,
        'sc_completion': sc_completion,
        'sc_completion_flag': sc_completion_flag,
        'sc_header': sc_header,
        'error_messages': error_messages
    }

    return render(request, 'Reports/Doc_report.html', context)


@login_required
def accnt_report(request):
    """
        :param request:
        :return:
        """

    client = getClients(request)
    final_list = []
    page_range = 0
    acc_value_array = get_account_assignvalues(request)
    account_desc_data_list = ''

    acc_cat_array = get_account_assignlist(request)
    company_array = get_companylist(request)
    lang_array = get_langlist(request)
    inp_acc_assgn_cat = acc_cat_array[0]
    inp_comp_code = int(company_array[0]['company_id'])
    inp_lang = 'EN'
    account_list = ''
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'comp_list': company_array,
        'lang_list': lang_array,
        'acct_val_list': acc_cat_array,
        'page_range': page_range,
        'inp_account_assgn_cat': acc_cat_array[0],
        'acc_value_array': acc_value_array,
        'inp_comp_code': inp_comp_code,
        'inp_lang': inp_lang,
    }

    if request.method == 'GET':
        # if 'final_list' in request.session:
        #     request.POST = request.session['final_list']
        inp_comp_code = int(company_array[0]['company_id'])
        inp_acc_assgn_cat = acc_cat_array[0]
        inp_lang = 'EN'

        if inp_comp_code is not None and inp_acc_assgn_cat is not None:
            account_list = AccountingData.objects.filter(client=client, company_id=inp_comp_code,
                                                         account_assign_cat=inp_acc_assgn_cat, del_ind=False)
        # print("account_list", account_list)
        result_array = []
        for account_data in account_list:
            # print("account_data", account_data)
            account_desc_data_list = AccountingDataDesc.objects.filter(client=client,
                                                                       company_id=account_data.company_id,
                                                                       del_ind=False,
                                                                       language_id=inp_lang,
                                                                       account_assign_value=account_data.account_assign_value,
                                                                       account_assign_cat=account_data.account_assign_cat)
            for data_acct_desc in account_desc_data_list:
                result_array.append(data_acct_desc.company_id)
                result_array.append(data_acct_desc.account_assign_cat)
                result_array.append(data_acct_desc.account_assign_value)
                result_array.append(data_acct_desc.description)
                result_array.append(data_acct_desc.language_id)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
                final_list.append(result_array)
        context['final_list'] = final_list
        return render(request, 'Reports/accnt_report.html', context)

    # If method is post get the form values and get header details accordingly
    if request.method == 'POST' or request.is_ajax():
        # request.method = 'POST'
        # data = JsonParser().get_json_from_req(request)
        inp_comp_code = request.POST.get('comp_code_app')
        inp_account_assgn_cat = request.POST.getlist('acc_assgn_cat')
        inp_lang = request.POST.get('language')

        if inp_comp_code is not None and inp_account_assgn_cat is not None:
            account_list = AccountingData.objects.filter(client=client, company_id=inp_comp_code,
                                                         account_assign_cat__in=inp_account_assgn_cat, del_ind=False)

        for account_data in account_list:
            account_desc_data_list = AccountingDataDesc.objects.filter(client=client,
                                                                       company_id=account_data.company_id,
                                                                       del_ind=False,
                                                                       language_id=inp_lang,
                                                                       account_assign_value=account_data.account_assign_value,
                                                                       account_assign_cat=account_data.account_assign_cat)
            result_array = []
            for data in account_desc_data_list:
                result_array.append(account_data.company_id)
                result_array.append(account_data.account_assign_cat)
                result_array.append(account_data.account_assign_value)
                result_array.append(data.description)
                result_array.append(data.language_id)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
                final_list.append(result_array)
        context['final_list'] = final_list
        t_count = len(final_list)

        # Context to display in Doc_report.html
        context = {
            'inc_nav': True,
            'inc_footer': True,
            'is_slide_menu': True,
            'comp_list': company_array,
            'lang_list': lang_array,
            'acct_val_list': acc_cat_array,
            # 'acct_rep_form' : acct_rep_form,
            'final_list': final_list,
            'page_range': page_range,
            't_count': t_count,
            'is_admin_active': True,
            'inp_account_assgn_cat': acc_cat_array[0],
            'acc_value_array': acc_value_array,
            'inp_comp_code': inp_comp_code,
            'inp_lang': inp_lang,
        }

    return render(request, 'Reports/accnt_report.html', context)


def get_acct_report(request):
    client = getClients(request)
    final_list = []
    page_range = 0
    account_desc_data_list = ''

    acc_cat_array = get_account_assignlist(request)
    company_array = get_companylist(request)
    lang_array = get_langlist(request)
    inp_acc_assgn_cat = acc_cat_array[0]
    account_list = ''

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'comp_list': company_array,
        'lang_list': lang_array,
        'acct_val_list': acc_cat_array,
        'page_range': page_range,
        'inp_account_assgn_cat': acc_cat_array[0]
    }

    if request.method == 'POST' and request.is_ajax():
        data = JsonParser().get_json_from_req(request)
        inp_comp_code = data['comp_code']
        inp_account_assgn_cat = data['selected_acct_assmt']
        inp_lang = data['lang']

        if inp_comp_code is not None and inp_account_assgn_cat is not None:
            account_list = AccountingData.objects.filter(client=client, company_id=inp_comp_code,
                                                         account_assign_cat__in=inp_account_assgn_cat, del_ind=False)

        result_array = []
        for account_data in account_list:
            account_desc_data_list = AccountingDataDesc.objects.filter(client=client,
                                                                       company_id=account_data.company_id,
                                                                       del_ind=False,
                                                                       language_id=inp_lang,
                                                                       account_assign_value=account_data.account_assign_value,
                                                                       account_assign_cat=account_data.account_assign_cat)
            for data in account_desc_data_list:
                result_array.append(account_data.company_id)
                result_array.append(account_data.account_assign_cat)
                result_array.append(account_data.account_assign_value)
                result_array.append(data.description)
                result_array.append(data.language_id)
                result_array.append(account_data.valid_from)
                result_array.append(account_data.valid_to)
                final_list.append(result_array)
            # return final_list

        context['final_list'] = final_list
        t_count = len(final_list)
        context['t_count'] = t_count
        # print("final_list", final_list)

        # Context to display in Doc_report.html
        # context = {
        #     'inc_nav': True,
        #     'inc_footer': True,
        #     'comp_list': company_array,
        #     'lang_list': lang_array,
        #     'acct_val_list': acc_cat_array,
        #     # 'acct_rep_form' : acct_rep_form,
        #     'final_list': final_list,
        #     'page_range': page_range,
        #     't_count': t_count,
        #     'is_slide_menu': True,
        #     'is_admin_active': True,
        #     'inp_account_assgn_cat': acc_cat_array[0]
        # }
    return render(request, 'Reports/accnt_report.html', context)


def org_announcements_search(request):
    encrypted_guid = []
    client = global_variables.GLOBAL_CLIENT
    status_dropdown_values = django_query_instance.django_filter_value_list_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'status'
    }, 'field_type_id')
    priority_dropdown_values = django_query_instance.django_filter_value_list_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'Priority'
    }, 'field_type_id')
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
    }

    if request.method == 'GET':
        announcement_result1 = OrgAnnouncements.objects.filter(client=client, del_ind=False)
        context['announcement_result1'] = announcement_result1
        return render(request, 'org_announcements_display.html', context)
    if request.method == 'POST':
        search_fields = {}
        for data in request.POST:
            if data != 'csrfmiddlewaretoken':
                value = request.POST[data]
                if data == 'block':
                    if value == 'on':
                        value = True
                    else:
                        value = False
                if value != '':
                    search_fields[data] = value

        search_fields['client'] = client
        search_fields['del_ind'] = False
        search_fields['status'] = request.POST.get('status')
        search_fields['priority'] = request.POST.get('priority')
        search_fields['announcement_subject'] = request.POST.get('announcement_subject')
        announcement_result1 = org_announcement_search(**search_fields)
        t_count = len(announcement_result1)

    for annsmt in announcement_result1:
        encrypted_guid.append(encrypt(annsmt['unique_announcement_id']))

    # print(encrypted_guid)
    context['announcement_result1'] = zip(announcement_result1, encrypted_guid)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_admin_active': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
        'announcement_result1': announcement_result1,
        't_count': t_count,
    }

    return render(request, 'org_announcements_display.html', context)


@login_required
def org_announcement_details(req, announcement_guid):
    """
    Gets the selected announcement details and render it in the Org Announcement details pop-up page
    :param announcement_guid:
    :param req: Form Request
    :return: Org Announcement details pop-up page
    """
    # supplier_id = decrypt(supplier_id)
    context = {}
    encrypted_guid = []
    update_user_info(req)
    annsmt_guid = decrypt(announcement_guid)
    announcement_details = django_query_instance.django_get_query(OrgAnnouncements,
                                                                  {'unique_announcement_id': announcement_guid})
    from_date = announcement_details.announcement_from_date.strftime("%Y-%m-%d")
    to_date = announcement_details.announcement_to_date.strftime("%Y-%m-%d")
    status_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'ACTIVE_INACTIVE'
    })
    priority_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'priority'
    })

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'announcement_details': announcement_details,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
        'from_date': from_date,
        'to_date': to_date
    }

    return render(req, 'org_announcement_details.html', context)


def delete_user(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    user_data = JsonParser_obj.get_json_from_req(request)
    user_info = django_query_instance.django_filter_query(UserData,
                                                          {'email__in': user_data['data'],
                                                           'del_ind': False}, None, None)
    for user in user_info:
        if django_query_instance.django_existence_check(ScHeader,
                                                        {'requester': user['username'],
                                                         'del_ind': False}) and user['object_id_id'] is not NULL:

            django_query_instance.django_update_query(UserData,
                                                      {'email': user['email'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})
        else:
            django_query_instance.django_filter_delete_query(UserData,
                                                             {'email': user['email'],
                                                              'client': global_variables.GLOBAL_CLIENT})
        success_message = "User deleted"

    employee_results = django_query_instance.django_filter_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)

    response = {'employee_results': employee_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def delete_supplier(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    supp_data = JsonParser_obj.get_json_from_req(request)
    supp_info = django_query_instance.django_filter_query(SupplierMaster,
                                                          {'supplier_id__in': supp_data['data'],
                                                           'del_ind': False}, None, None)
    for supp in supp_info:
        if django_query_instance.django_existence_check(OrgSuppliers,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}):
            django_query_instance.django_update_query(ScItem,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})
        if django_query_instance.django_existence_check(OrgSuppliers,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}) and \
                django_query_instance.django_existence_check(ScItem,
                                                             {'supplier_id__in': supp['data'],
                                                              'del_ind': False}):
            django_query_instance.django_update_query(OrgSuppliers,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})

        if not django_query_instance.django_existence_check(OrgSuppliers,
                                                            {'supplier_id__in': supp['data'],
                                                             'del_ind': False}) and \
                django_query_instance.django_existence_check(ScItem,
                                                             {'supplier_id__in': supp['data'],
                                                              'del_ind': False}):
            django_query_instance.django_update_query(OrgSuppliers,
                                                      {'supplier_id__in': supp['data'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True})
        if django_query_instance.django_existence_check(SupplierMaster,
                                                        {'supplier_id__in': supp['data'],
                                                         'del_ind': False}) and \
                not django_query_instance.django_existence_check(OrgSuppliers,
                                                                 {'supplier_id__in': supp['data'],
                                                                  'del_ind': False}) and \
                not django_query_instance.django_existence_check(ScItem,
                                                                 {'supplier_id__in': supp['data'],
                                                                  'del_ind': False}):
            django_query_instance.django_filter_delete_query(SupplierMaster,
                                                             {'supplier_id__in': supp['data'],
                                                              'client': global_variables.GLOBAL_CLIENT})
        success_message = "Supplier deleted"

    employee_results = django_query_instance.django_filter_query(SupplierMaster, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)

    response = {'employee_results': employee_results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def delete_org_announcement(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    success_message = ''
    annsmt_data = JsonParser_obj.get_json_from_req(request)
    # org_info = django_query_instance.django_filter_query(UserData,
    #                                                       {'email__in': user_data['data'],
    #                                                        'del_ind': False}, None, None)
    # print(annsmt_data)
    announcement_details = django_query_instance.django_get_query(OrgAnnouncements,
                                                                  {'unique_announcement_id': annsmt_data})
    if django_query_instance.django_existence_check(OrgAnnouncements,
                                                    {'announcement_id__in': annsmt_data,
                                                     'del_ind': False}):
        django_query_instance.django_update_query(OrgAnnouncements,
                                                  {'announcement_id__in': annsmt_data,
                                                   'client': global_variables.GLOBAL_CLIENT},
                                                  {'del_ind': True})
        success_message = "Org Announcement deleted"

    results = django_query_instance.django_filter_query(OrgAnnouncements, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, None, None)

    response = {'results': results, 'success_message': success_message}
    return JsonResponse(response, safe=False)


def lock_unlock_emp(request):
    """
    """
    emp_lock_flag_detail = JsonParser_obj.get_json_from_req(request)
    status = emp_lock_flag_detail['employee_id'].split('-')[1]
    empId = emp_lock_flag_detail['employee_id'].split('-')[0]
    if status in ('LOCKED', 'UNLOCKED'):
        django_query_instance.django_update_query(UserData,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'employee_id': empId,
                                                   'del_ind': False},
                                                  {'user_locked': emp_lock_flag_detail['flag']})
    if status in ('PWDLOCKED', 'PWDUNLOCKED'):
        django_query_instance.django_update_query(UserData,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'employee_id': empId,
                                                   'del_ind': False},
                                                  {'pwd_locked': emp_lock_flag_detail['flag']})
    response = {}
    return JsonResponse(response, safe=False)


def get_username(request):
    user_data = JsonParser_obj.get_json_from_req(request)
    if user_data:
        username = get_user_id_by_email_id(user_data)

    return JsonResponse(username, safe=False)


def extract_employee_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Employee_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['EMAIL', 'USERNAME', 'PERSON_NO', 'FORM_OF_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'PHONE_NUM', 'PASSWORD',
         'DATE_JOINED', 'FIRST_LOGIN', 'LAST_LOGIN', 'IS_ACTIVE', 'IS_SUPERUSER', 'IS_STAFF', 'DATE_FORMAT',
         'EMPLOYEE_ID', 'DECIMAL_NOTATION', 'USER_TYPE', 'LOGIN_ATTEMPTS', 'USER_LOCKED', 'PWD_LOCKED', 'SSO_USER',
         'VALID_FROM', 'VALID_TO', 'del_ind', 'CURRENCY_ID', 'LANGUAGE_ID', 'OBJECT_ID', 'TIME_ZONE'])

    return response


def application_monitoring(request):
    """

    """
    update_user_info(request)
    application_monitoring_form = ApplicationMonitoringForm()
    sc_header_list = django_query_instance.django_filter_query(ScHeader,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'transmission_error': True}, None, None)
    for sc_header in sc_header_list:
        sc_header['encrypted_header_guid'] = encrypt(sc_header['guid'])

    inp_doc_type = 'SC'
    context = {
        'application_monitoring_form': application_monitoring_form,
        'sc_header_list': sc_header_list,
        'inp_doc_type': inp_doc_type,
        'is_slide_menu': True,
        'is_admin_active': True,
        'inc_nav': True,
        'inc_footer': True,
        'sc_completion_flag': False
    }
    return render(request, 'ApplicationMonitoring/application_monitoring.html', context)


def email_user_monitoring(request):
    """

    """
    global t_count, email_list, inp_email_type, inp_email_status, num
    update_user_info(request)
    email_user_monitoring_form = EmailUserMonitoringForm()
    final_data = []
    final_data1 = []
    email_list = ''
    inp_email_type = ''
    inp_email_status = 0
    error_messages = ''

    if request.method == 'GET':
        inp_email_type = 'REGISTRATION'
        inp_email_status = 2
        email_list = django_query_instance.django_filter_query(EmailUserMonitoring,
                                                               {'client': global_variables.GLOBAL_CLIENT,
                                                                'object_type': inp_email_type, 'email_status': inp_email_status,
                                                                'del_ind': False}, None, None)

        t_count = len(email_list)
        context = {
            'email_user_monitoring_form': email_user_monitoring_form,
            'email_data': email_list,
            'inp_email_type': inp_email_type,
            'inp_email_status': inp_email_status,
            't_count': t_count,
            'is_slide_menu': True,
            'is_admin_active': True,
            'inc_nav': True,
            'inc_footer': True,
            'sc_completion_flag': False
        }
        return render(request, 'ApplicationMonitoring/email_user_monitoring.html', context)
    num = 0
    if request.method == 'POST' or request.is_ajax():
        email_user_monitoring_form = EmailUserMonitoringForm(request.POST)
        t_count = 0
        inp_email_type = request.POST.get('email_types')
        inp_email_status = request.POST.get('email_status')
        inp_from_date = request.POST.get('from_date')
        inp_to_date = request.POST.get('to_date')
        num = int(inp_email_status)

        if inp_email_type is not None:
            email_list = list(EmailUserMonitoring.objects.filter(
                client=global_variables.GLOBAL_CLIENT,
                object_type=inp_email_type, email_status=num,
                del_ind=False,
                email_user_monitoring_created_at__gte=inp_from_date,
                email_user_monitoring_created_at__lte=inp_to_date
            ).values())

            final_data1.append(email_list)
            t_count = len(email_list)

        context = {
            'email_user_monitoring_form': email_user_monitoring_form,
            'email_data': email_list,
            'inp_email_type': inp_email_type,
            'inp_email_status': int(inp_email_status),
            't_count': t_count,
            'status': num,
            'is_slide_menu': True,
            'is_admin_active': True,
            'inc_nav': True,
            'inc_footer': True,
            'error_messages': error_messages
        }
        return render(request, 'ApplicationMonitoring/email_user_monitoring.html', context)
