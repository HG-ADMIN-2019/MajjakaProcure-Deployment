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
import json

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
from eProc_Registration.Utilities.registration_generic import save_supplier_image, save_supplier_data
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Suppliers.models.suppliers_model import OrgSuppliers

django_query_instance = DjangoQueries()


@login_required
@transaction.atomic
def update_suppliers_basic_details(request):
    message = ''
    update_user_info(request)
    if request.method == 'POST':
        print(request.FILES)
        message, encrypted_supp = save_supplier_data(request)

        if 'supplier_image' in request.FILES:
            supplier_file = request.FILES['supplier_image']
            supplier_id = request.POST['supplier_id']
            supplier_image_name = request.FILES['supplier_image'].name
            save_supplier_image(supplier_file, supplier_id, supplier_image_name)

    return JsonResponse({'message': message,'encrypted_supplier':encrypted_supp})


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
