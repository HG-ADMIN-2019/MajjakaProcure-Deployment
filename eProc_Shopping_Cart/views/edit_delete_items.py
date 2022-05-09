"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    edit_delete.py
Usage:
     update_item         - Used to update an item in the cart
     delete_item         - Used to delete an item from the cart
     empty_shopping_cart - Used to empty all the items in the shopping cart

Author:
    Sanjay
"""
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from eProc_Add_Item.Utilities.add_item_specific import update_create_free_text
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getUsername, getClients, display_cart_counter
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG156
from eProc_Configuration.models import FreeTextForm
from eProc_Form_Builder.Utilities.form_builder_generic import FormBuilder
from eProc_Form_Builder.models import EformData, EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_total_value, \
    calculate_item_price
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import check_for_eform, get_limit_update_content, \
    get_free_text_content
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()
JsonParser_obj = JsonParser()


@transaction.atomic
def update_item(request):
    """
    :param request:
    :return:
    """
    guid = request.POST.get("guid")
    update_user_info(request)
    product_category_id = request.POST.get('product_category_id')
    if django_query_instance.django_existence_check(CartItemDetails, {'pk': guid}):
        item_details = django_query_instance.django_get_query(CartItemDetails, {'pk': guid})
    else:
        item_details = django_query_instance.django_existence_check(ScItem, {'pk': guid})
        if item_details:
            item_details = django_query_instance.django_get_query(ScItem, {'pk': guid})

    # Catalogue context
    if item_details.call_off == CONST_CO01:
        quantity = item_details.quantity
        if not quantity:
            quantity = item_details.catalog_qty
        catalog_context = {
            'catalog_quantity': quantity,
            'price': item_details.price,
        }
        return JsonResponse(catalog_context)

    # Limit order context
    if item_details.call_off == CONST_CO04:
        limit_context = get_limit_update_content(item_details)
        return JsonResponse(limit_context)

    # PR context
    if item_details.call_off == CONST_CO03:
        pr_context = {
            'item_name': item_details.description,
            'item_long_desc': item_details.long_desc,
            'prod_desc': item_details.prod_cat_desc,
            'prod_id': item_details.ext_product_id,
            'prod_cat_id': item_details.prod_cat,
            'price': item_details.price,
            'currency': item_details.currency,
            'unit': item_details.unit,
            'lead_time': item_details.lead_time,
            'quantity': item_details.quantity
        }
        return JsonResponse(pr_context)

    # freetext context
    if item_details.call_off == CONST_CO02:
        free_text_context = {
            'is_eform': False,
            'item_name': item_details.description,
            'prod_desc': item_details.prod_cat_desc,
            'item_long_desc': item_details.long_desc,
            'price': item_details.price,
            'price_unit': item_details.price_unit,
            'unit': item_details.unit,
            'del_date': item_details.item_del_date,
            'quantity': item_details.quantity,
            'supp_id': item_details.supplier_id,
            'currency_id':item_details.currency
        }
        supplier = item_details.supplier_id
        freetext_id = django_query_instance.django_filter_value_list_query(CartItemDetails,
                                                                           {'guid': guid},
                                                                           'int_product_id')[0]
        configured_freetext_form, eform_configured = FormBuilder().get_freetext_form(freetext_id)
        for eform_data in eform_configured:
            if django_query_instance.django_existence_check(EformFieldData,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'cart_guid': guid,
                                                             'eform_field_count': eform_data['eform_field_count']}):
                eform_data['user_field_data'] = django_query_instance.django_filter_value_list_query(EformFieldData,
                                                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                                                         'cart_guid': guid,
                                                                                                         'eform_field_count':
                                                                                                             eform_data[
                                                                                                                 'eform_field_count']},
                                                                                                     'eform_field_data')[0]
                eform_data['eform_transaction_guid'] = django_query_instance.django_filter_value_list_query(EformFieldData,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'cart_guid': guid,
                                                                      'eform_field_count':eform_data['eform_field_count']},
                                                                     'eform_field_data_guid')[0]
        check = check_for_eform(request)
        if supplier not in check:
            free_text_context['is_eform'] = True
            eform = get_free_text_content(guid)
            free_text_context.update(eform)

        return JsonResponse({'free_text_context': free_text_context,
                             'configured_eform_fields': configured_freetext_form,
                             'eform_configured': eform_configured})
    return JsonResponse({'message': MSG156})


# Function to update freetext item
@transaction.atomic
def update_free_text_item(request):
    """
    :param request:
    :return:
    """
    call_off = CONST_CO02
    catalog_qty = None
    lot_size = 1
    if request.method == 'POST':
        free_text_fields = []
        eform = request.POST.get('eform')
        guid = request.POST.get('guid')
        item_name = request.POST.get('item_name')
        prod_desc = request.POST.get('prod_desc')
        price = request.POST.get('price')
        uom = request.POST.get('unit')
        del_date = request.POST.get('del_date')
        quantity = request.POST.get('quantity')
        supp_id = request.POST.get('supp_id')

        free_text_fields.append(eform)
        free_text_fields.append(guid)
        free_text_fields.append(item_name)
        free_text_fields.append(prod_desc)
        free_text_fields.append(price)
        free_text_fields.append(uom)
        free_text_fields.append(del_date)
        free_text_fields.append(quantity)
        free_text_fields.append(supp_id)

        # To get eform fields if True
        if eform == 'true':
            field_value1 = request.POST.get('form_field1')
            field_value2 = request.POST.get('form_field2')
            field_value3 = request.POST.get('form_field3')
            field_value4 = request.POST.get('form_field4')
            field_value5 = request.POST.get('form_field5')
            field_value6 = request.POST.get('form_field6')
            field_value7 = request.POST.get('form_field7')
            field_value8 = request.POST.get('form_field8')
            field_value9 = request.POST.get('form_field9')
            field_value10 = request.POST.get('form_field10')
            form_id = django_query_instance.django_get_query(FreeTextForm,
                                                             {'supp_id': supp_id, 'client': getClients(request)})
            # Appending eform data
            free_text_fields.append(field_value1)
            free_text_fields.append(field_value2)
            free_text_fields.append(field_value3)
            free_text_fields.append(field_value4)
            free_text_fields.append(field_value5)
            free_text_fields.append(field_value6)
            free_text_fields.append(field_value7)
            free_text_fields.append(field_value8)
            free_text_fields.append(field_value9)
            free_text_fields.append(field_value10)
            free_text_fields.append(form_id)

        update_create_free_text(free_text_fields, request)
        item_value = calculate_item_total_value(call_off, quantity, catalog_qty, lot_size, price, overall_limit=None)
        total_value = calculate_total_value(request)

        return JsonResponse({'item_value': item_value, 'total_value': total_value})


# Function to delete single items from the cart
@transaction.atomic
def delete_item(request):
    """
    :param request: Takes the request from the user and delete an item from the cart
    :return: After deleting an item returns back to sc_first_step.html
    """
    update_user_info(request)
    guid = request.POST.get('guid')
    item_details = django_query_instance.django_get_query(CartItemDetails, {'pk': guid})
    if item_details.eform_id:
        django_query_instance.django_filter_delete_query(EformFieldData,
                                                         {'cart_guid': guid})
    item_details.delete()
    cart_length = display_cart_counter(global_variables.GLOBAL_LOGIN_USERNAME)
    # If call_off type is free text delete the eform data
    if item_details.call_off == CONST_CO02:
        if django_query_instance.django_existence_check(EformData, {'cart_guid': guid}):
            eform_data = django_query_instance.django_get_query(EformData, {'cart_guid': guid})
            eform_data.delete()
    if item_details.call_off == CONST_CO01:
        if django_query_instance.django_existence_check(EformFieldData, {'cart_guid': guid}):
            eform_data = django_query_instance.django_get_query(EformFieldData, {'cart_guid': guid})
            eform_data.delete()
    return JsonResponse({'message': cart_length})


# Function Delete all items in shopping cart
@login_required
@transaction.atomic
def empty_shopping_cart(request):
    """
    :param request: Takes request from the user and empty all the items in the shopping cart w.r.t user
    :return: After deleting an item returns back to home.html
    """
    item_details = django_query_instance.django_filter_only_query(CartItemDetails, {
        'username': getUsername(request), 'client': getClients(request)
    })
    for eform_guid in item_details:
        django_query_instance.django_filter_delete_query(EformData, {'cart_guid': eform_guid.guid})
    item_details.delete()
    return HttpResponseRedirect('/shop/products_services/All/create')


@transaction.atomic
def update_catalog_item(request):
    update_user_info(request)
    call_off = CONST_CO01
    catalog_qty = None
    lot_size = 1
    json_data = JsonParser_obj.get_json_from_req(request)
    guid = json_data['guid']
    quantity = json_data['quantity']
    price = json_data['price']
    item_price = calculate_item_price(guid, quantity)
    item_value = calculate_item_total_value(call_off, quantity, catalog_qty, lot_size, item_price, overall_limit=None)
    defaults = {
        'guid': guid,
        'quantity': quantity,
        'price': item_price
    }
    django_query_instance.django_update_or_create_query(CartItemDetails, {'guid': guid}, defaults)
    total_value = calculate_total_value(global_variables.GLOBAL_LOGIN_USERNAME)
    return JsonResponse({'item_price': item_price, 'item_value': item_value, 'total_value': total_value})
