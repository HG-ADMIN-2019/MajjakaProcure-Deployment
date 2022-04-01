"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    purchaser_cockpit.py
Usage:
    Purchase assist role user data
Author:
    Deepika K
"""
from django.shortcuts import render
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Purchaser_Cockpit.Utilities.purchaser_cockpit_specific import filter_based_on_sc_item_field


def incomplete_form(request, guid=None):
    """

    :param request:
    :param guid:
    :return:
    """
    context = {
        'inc_nav': True,
        'shopping': True,
    }

    return render(request, 'Purchaser_Cockpit/incomplete_form.html', context)


def sc_item_field_filter(request):
    supplier_id = False
    comp_code = False
    prod_cat = False
    client = getClients(request)
    order_list = []

    if request.method == 'POST':
        prod_cat = request.POST.get('prod_cat')
        supplier_id = request.POST.get('supplier_id')
        comp_code = request.POST.get('comp_code')
        if prod_cat:
            order_list.append(prod_cat)
        if supplier_id:
            order_list.append(supplier_id)
        if comp_code:
            order_list.append(comp_code)

    sc_header_item_details = filter_based_on_sc_item_field(client, order_list)

    context = {
        'sc_header_item_details': sc_header_item_details,
        'prod_cat': prod_cat,
        'supplier_id': supplier_id,
        'comp_code': comp_code,
        'inc_nav': True,
        'shopping': True,
        'is_slide_menu': True
    }

    return render(request, 'Purchaser_Cockpit/sc_item_field_filter.html', context)
