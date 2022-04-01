"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    application_settings.py
Usage:
     app_setting           - Renders application settings home page where the user is allowed to configure settings
     create_number_ranges  - Creates new number ranges and saves the data to DB through ajax calls
     edit_number_ranges    - Edit number ranges and saves the data to DB through ajax calls
Author:
    Sanjay
"""

import io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.str_concatenate import split_str
from eProc_Configuration.models import *
from eProc_Attributes.views import JsonParser_obj
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_country_data
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from django.core import serializers
from django.http import JsonResponse
from eProc_Configuration.Utilities.application_settings_specific import save_app_data_into_db, \
    save_calendar_data_into_db, save_actasmt_data_into_db, save_messageId_data_into_db, save_messageIdDesc_data_into_db, \
    save_calendarholiday_data_into_db, \
    save_calendar_data_into_db, \
    save_documenttype_data_into_db, save_transactiontype_data_into_db
from eProc_Configuration.Utilities.application_settings_specific import save_app_data_into_db, save_client_data_into_db, \
    save_number_range_data_into_db
from eProc_Master_Settings.Utilities.master_settings_specific import save_orgnode_types_data_into_db, \
    save_orgattributes_data_into_db, save_authorobject_data_into_db, save_auth_group_data_into_db, \
    save_roles_data_into_db, save_auth_data_into_db
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_basic_pk_fk_tables import UploadPkFkTables
from eProc_Upload.Utilities.upload_data.upload_pk_tables import CompareTableHeader, MSG048
from eProc_Basic_Settings.Utilities.basic_settings_specific import csv_data_arrangement, csv_preview_data, \
    save_prodcat_data_into_db
import csv

django_query_instance = DjangoQueries()


@login_required
def app_setting(request):
    """
    :param request: Gets the configured number ranges from the database and displays.
    :return: Renders application_settings.html where the user is allowed to create, edit, display the number ranges
    """
    return render(request, 'Application_Settings/application_settings.html')


def app_setting_latest(request):
    """
    :param request: Gets the configured number ranges from the database and displays.
    :return: Renders application_settings.html where the user is allowed to create, edit, display the number ranges
    """
    return render(request, 'Application_Settings/app_settings.html', {'inc_nav': True})


def create_update_application_data(request):
    """

    """
    update_user_info(request)
    app_data = JsonParser_obj.get_json_from_req(request)
    if app_data['table_name'] == 'OrgClients':
        display_data = save_client_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'UnspscCategories':
        display_data = save_prodcat_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgNodeTypes':
        display_data = save_orgnode_types_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'OrgAttributes':
        display_data = save_orgattributes_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AuthorizationObject':
        display_data = save_authorobject_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AuthorizationGroup':
        display_data = save_auth_group_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'UserRoles':
        display_data = save_roles_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'Authorization':
        display_data = save_auth_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'CalenderConfig':
        display_data = save_calendar_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'DocumentType':
        display_data = save_documenttype_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'TransactionTypes':
        display_data = save_transactiontype_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'CalenderHolidays':
        display_data = save_calendarholiday_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'AccountAssignmentCategory':
        display_data = save_actasmt_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'MessagesId':
        display_data = save_messageId_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'MessagesIdDesc':
        display_data = save_messageIdDesc_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)
    if app_data['table_name'] == 'NumberRanges':
        display_data = save_number_range_data_into_db(app_data)
        return JsonResponse(display_data, safe=False)


def save_app_settings_data(request):
    """

    :param request:
    :return:
    """

    update_user_info(request)
    client = getClients(request)
    basic_data = JsonParser().get_json_from_req(request)
    Table_name = basic_data['Dbl_clck_tbl_id']
    del basic_data['Dbl_clck_tbl_id']

    basic_data_list = []

    for value in basic_data.values():
        basic_data_list.append(value)

    upload_data_response = save_app_data_into_db(basic_data_list, Table_name, client)
    return JsonResponse(upload_data_response, safe=False)


def data_upload_fk(request):
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('utf8')
    # fin_upload_data = io.StringIO(data_set_val)
    upload_csv = CompareTableHeader()
    result = {}
    # upload_csv.header_data = io.StringIO(data_set_val)
    upload_csv.app_name = request.POST.get('appname')
    upload_csv.table_name = request.POST.get('Tablename')
    upload_csv.request = request
    fin_data_upload_header = io.StringIO(data_set_val)
    upload_csv.header_data = fin_data_upload_header
    basic_save,header_detail = upload_csv.basic_header_condition()
    # if not basic_save:
    try:
        result['error_message'], result['data'] = upload_csv.csv_preview_data(header_detail, data_set_val)
        # correct_order_list = csv_preview_data(header_detail, data_set_val)
        # retrieving correct ordered data from csv_data_arrangement() - basic_settings_specific.py
        # correct_order_list = csv_data_arrangement(db_header, data_set_val)
        return JsonResponse(result, safe=False)

    except MultiValueDictKeyError:
        csv_file = False
        messages.error(request, MSG048)

    # else:
    return JsonResponse(basic_save, safe=False)


def save_catalog_data(request):
    """

    :param request:
    :return:
    """
    catalog_data = JsonParser_obj.get_json_from_req(request)
    for data in catalog_data:
        if not (
                Catalogs.objects.filter(catalog_id=data['catalog_id'], name=data['name'],
                                        description=data['description'],
                                        product_type=data['product_type']).exists()):
            obj, created = Catalogs.objects.update_or_create(client=OrgClients.objects.get(client=getClients(request)),
                                                             catalog_guid=guid_generator(),
                                                             catalog_id=data['catalog_id'],
                                                             name=data['name'],
                                                             description=data['description'],
                                                             product_type=data['product_type'])
    catalog_data_response = Catalogs.objects.filter(del_ind=False)
    return JsonParser_obj.get_json_from_obj(catalog_data_response)


def save_productservice_data(request):
    """

    :param request:
    :return:
    """
    client = getClients(request)
    product_data = JsonParser_obj.get_json_from_req(request)
    product_not_exist: object = ProductsDetail.objects.filter(del_ind=False).exclude(
        product_id__in=[product['product_id'] for product in product_data])

    for set_del_int in product_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()
    for data in product_data:
        if not (ProductsDetail.objects.filter(product_id=data['product_id']).exists()):
            country_of_origin = data['country_of_origin']
            country = Country.objects.get(country_code=country_of_origin)
            obj, created = ProductsDetail.objects.update_or_create(client=OrgClients.objects.get(client=client),
                                                                   catalog_item=guid_generator(),
                                                                   product_id=int(data['product_id']),
                                                                   short_desc=data['short_desc'],
                                                                   long_desc=data['long_desc'],
                                                                   supplier_id=data['supplier_id'],
                                                                   prod_cat_id=data['prod_cat_id'],
                                                                   catalog_id=data['catalog_id'],
                                                                   product_type=data['product_type'],
                                                                   price_on_request=False,
                                                                   unit=UnitOfMeasures.objects.get(uom_id=data['unit']),
                                                                   price_unit=data['price_unit'],
                                                                   currency=Currency.objects.get(
                                                                       currency_id=data['currency']),
                                                                   price=data['price'],
                                                                   manufacturer=data['manufacturer'],
                                                                   manu_prod=data['manu_prod'],
                                                                   unspsc=UnspscCategories.objects.get(
                                                                       prod_cat_id=data['unspsc']),
                                                                   brand=data['brand'], lead_time=data['lead_time'],
                                                                   quantity_avail=data['quantity_avail'],
                                                                   quantity_min=data['quantity_min'],
                                                                   offer_key=data['offer_key'],
                                                                   country_of_origin=country,
                                                                   language=Languages.objects.get(
                                                                       language_id=data['language']),
                                                                   search_term1=data['search_term1'],
                                                                   search_term2=data['search_term2'])
    catalog_data_response = ProductsDetail.objects.filter(client=client, del_ind=False)
    return JsonParser_obj.get_json_from_obj(catalog_data_response)


def check_data_fk(request):
    if request.is_ajax():
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        db_header_data = table_data__array['db_header_data']
        client = getClients(request)
        print(client)
        check_data_class = UploadPkFkTables()
        check_data_class.app_name = table_data__array['appname']
        check_data_class.table_name = table_data__array['Tablename']

        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = check_data_class.basic_table_new_conditions(popup_data_list, db_header_data, client)
        return JsonResponse(check_variable)

    return render(request, 'Application_Settings/Basic_setting_Upload/upload_countries.html')


def test():
    def monday():
        return "monday"

    def tuesday():
        return "tuesday"

    def wednesday():
        return "wednesday"

    def thursday():
        return "thursday"

    def friday():
        return "friday"

    def saturday():
        return "saturday"

    def sunday():
        return "sunday"

    def default():
        return "Invalid day"

    def switch(wday):
        switcher = {
            1: monday,
            2: tuesday,
            3: wednesday,
            4: thursday,
            5: friday,
            6: saturday,
            7: sunday
        }





def weekday(num):
    switch = {
        '1': 'Sun',
        '2': 'Mon',
        '3': 'Tue',
        '4': 'Wed',
        '5': 'Thur',
        '6': 'Fri',
        '7': 'Sat'
    }
    return switch.get(num, "Invalid input")


def get_holiday_from_calenderid(request):
    # if request.is_ajax():
    calender_id = request.POST.get('calender_id')
    # holiday_array = JsonParser_obj.get_json_from_req(request)
    # calender_id = holiday_array['calender_id']
    holidays_data = CalenderHolidays.objects.filter(del_ind=False, calender_id=calender_id)
    qs_json = serializers.serialize('json', holidays_data)
    return HttpResponse(qs_json, content_type='application/json')


def basic_settings(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Basic_Data_Configuration/basic_data_configuration.html', context)


def application_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Application_Data_Configuration/application_data_configuration.html', context)


def master_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Master_Data_Configuration/master_data_configuration.html', context)


def transaction_data_configuration(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'Transaction_Data_Configuration/transaction_data_configuration.html', context)

# def dropdown_document_type(request):
#   update_user_info(request)
# client = global_variables.GLOBAL_CLIENT

# shopping_cart = django_query_instance.django_filter_only_query(FieldTypeDesc, {
#    'client': client, 'del_ind': False, 'document_type': 'DOC01'
# })
# context = {
#     'shopping_cart': shopping_cart,
# }
#  return render(request, 'Application_Settings/upload_document_type.html', context)
