"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        supplier_details.py
    Usage:
        Story SP12-10
        Function to get the supplier details
        Taking the supplier id and getting details and rendering back to the supplier details pop-up page
        We have the function to save the changes in Supplier details pop-up back to the data base
     Author:
        Varsha Prasad
"""
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG177, MSG178
from eProc_Configuration.models import *
from eProc_Registration.Utilities.registration_generic import save_supplier_image
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Suppliers.models.suppliers_model import OrgSuppliers

django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def update_suppliers_basic_details(request):
    update_user_info(request)
    if request.method == 'POST':
        print(request.FILES)
        if 'supplier_image' in request.FILES:
            supplier_file = request.FILES['supplier_image']
            supplier_id = request.POST['supplier_id']
            supplier_image_name = request.FILES['supplier_image'].name
            save_supplier_image(supplier_file, supplier_id, supplier_image_name)
        update_supplier_guid = request.POST.get('supplier_guid')
        update_name1 = request.POST.get('name1')
        update_name2 = request.POST.get('name2')
        update_language_id = request.POST.get('language_id')
        update_city_id = request.POST.get('city_id')
        update_postal_code_id = request.POST.get('postal_code_id')
        update_street_id = request.POST.get('street_id')
        update_country_code_id = request.POST.get('country_code_id')
        update_currency_id = request.POST.get('currency_id')
        update_landline_id = request.POST.get('landline_id')
        update_mobile_num_id = request.POST.get('mobile_num_id')
        update_fax_id = request.POST.get('fax_id')
        update_email_id = request.POST.get('email_id')
        update_search_term1_id = request.POST.get('search_term1_id')
        update_search_term2_id = request.POST.get('search_term2_id')
        update_working_days_id = request.POST.get('working_days_id')
        update_duns_number_id = request.POST.get('duns_number_id')
        update_email1_id = request.POST.get('email1_id')
        update_email2_id = request.POST.get('email2_id')
        update_email3_id = request.POST.get('email3_id')
        update_email4_id = request.POST.get('email4_id')
        update_email5_id = request.POST.get('email5_id')
        update_output_medium_id = request.POST.get('output_medium_id')

        update_supplier_basic_data = django_query_instance.django_filter_only_query(SupplierMaster,
                                                                                    {'supp_guid': update_supplier_guid,
                                                                                     'del_ind': False})
        update_supplier_basic_data.update(
            name1=update_name1,
            name2=update_name2,
            language_id=update_language_id,
            city=update_city_id,
            postal_code=update_postal_code_id,
            street=update_street_id,
            country_code=update_country_code_id,
            currency_id=update_currency_id,
            landline=update_landline_id,
            mobile_num=update_mobile_num_id,
            fax=update_fax_id,
            email=update_email_id,
            email1=update_email1_id,
            email2=update_email2_id,
            email3=update_email3_id,
            email4=update_email4_id,
            email5=update_email5_id,
            output_medium=update_output_medium_id,
            search_term1=update_search_term1_id,
            search_term2=update_search_term2_id,
            duns_number=update_duns_number_id,
            working_days=update_working_days_id,
        )

    return JsonResponse({'message': MSG177})


@transaction.atomic
def update_supplier_purch_details(request):
    supp_org_data = JsonParser().get_json_from_req(request)
    for org_data in supp_org_data:
        django_query_instance.django_filter_delete_query(OrgSuppliers, {'guid__in': org_data['delete_supplier']})
        guid = org_data['supp_org_guid']
        if guid == '':
            guid = guid_generator()
        defaults = {
            'supplier_id': org_data['supp_id'],
            'payment_term_key': org_data['payment_term'],
            'incoterm_key': django_query_instance.django_get_query(Incoterms, {'incoterm_key': org_data['incoterm']}),
            'currency_id': django_query_instance.django_get_query(Currency, {'pk': org_data['currency_id']}),
            'gr_inv_vrf': org_data['gr_inv_vrf'],
            'inv_conf_exp': org_data['inv_conf_exp'],
            'gr_conf_exp': org_data['gr_conf_exp'],
            'po_resp': org_data['po_resp'],
            'ship_notif_exp': org_data['ship_notif_exp'],
            'purch_block': org_data['purch_block'],
            'porg_id': org_data['porg_id'],
            'client_id': getClients(request)
        }
        django_query_instance.django_update_or_create_query(OrgSuppliers, {'guid': guid}, defaults)

    return JsonResponse({'message': MSG178})
