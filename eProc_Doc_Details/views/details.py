"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        Details.py
    Usage:
        Story SP08-27
        Function to get the deatils of the document (SC/PO}
        Taking the guid and getting details using the functions of utils class and rendering back to the DocDetails page
     Author:
        Deepika,Shilpa Ellur, Sanjay
"""
import datetime
import json
import shutil
from django.contrib.auth.decorators import login_required
from django.db import transaction

from eProc_Account_Assignment.Utilities.account_assignment_generic import AccountAssignment, get_header_level_gl_acc, \
    get_acc_value_and_description_append, AccountAssignmentCategoryDetails
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.get_system_setting_attributes import *
from eProc_Basic.Utilities.functions.ignore_duplicates import remove_duplicate_element_array
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.decorators import authorize_view
from eProc_Doc_Details.Utilities.update_saved_item import UpdateSavedItem
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_sc_header_app
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes
from eProc_User_Settings.Utilities.user_settings_specific import append_attrlow_desc
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.type_casting import type_cast_array_float_to_str
from eProc_Doc_Details.Utilities.details_generic import GetAttachments, update_approval_status, update_sc_data, \
    get_doc_details, update_eform_scitem
from eProc_Doc_Details.Utilities.details_specific import *
from eProc_Notes_Attachments.Utilities.notes_attachments_generic import download
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_item_price
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.limit_form import UpdateLimitItem
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_supplier_first_second_name, get_prod_cat, \
    get_prod_by_id, update_eform_details_scitem
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_manger_detail, get_prod_cat_dropdown, \
    get_users_first_name, update_supplier_uom_for_prod, update_supplier_uom
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader, ScApproval, ScItem, PurchasingUser, ScPotentialApproval
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Basic.Utilities.constants.constants import *
from Majjaka_eProcure import settings
from eProc_Notes_Attachments.models import Attachments
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import SaveShoppingCart
from eProc_Shopping_Cart.context_processors import update_user_obj_id_list_info
from eProc_User_Settings.Utilities.user_settings_generic import get_attr_value
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_gl_account_default_value
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Workflow.Utilities.work_flow_generic import save_sc_approval

JsonParser_obj = JsonParser()


@login_required
@authorize_view(CONST_MY_ORDER)
def my_order_doc_details(req, flag, type, guid, mode, access_type):
    """
    Gets the details from various tables and reders back to the details page
    :param mode:
    :param flag:
    :param req: Form Request
    :param type: Consists of type od document SC/PO
    :param guid: Document guid for which the details have to be pulled
    :return: Doc details page
    """
    # initializations
    sc_item_list = []
    # client = getClients(req)
    # sys_attributes_instance = sys_attributes(client)
    item_detail_list = []
    gl_acc_num_list = []
    item_value_list = []
    sc_header_instance = {}
    total_value_of_item_converted = []
    requesters_currency = ''
    total_val = 0
    template = 'Doc_Details/my_order_doc_details.html'
    # To validate access based on creator and requester
    update_user_info(req)
    header_guid = decrypt(guid)
    # get shopping cart related data based on header guid
    doc_data = get_doc_details(type, header_guid)
    sc_hdr_details = doc_data.get('hdr_data', None)
    sc_item_details = doc_data.get('itm_data', None)
    sc_accounting_details = doc_data.get('acc_data', None)
    sc_approval_data = doc_data.get('appr_data', None)
    sc_address_data = doc_data.get('addr_data', None)
    sc_header, sc_appr, sc_completion, requester_first_name = get_sc_header_app(sc_hdr_details,
                                                                                client=global_variables.GLOBAL_CLIENT)
    # get supplier, internal and approval notes
    supp_notes = get_item_notes(header_guid, CONST_SUPPLIER_NOTE, True)
    int_notes = get_item_notes(header_guid, CONST_INTERNAL_NOTE, True)
    appr_notes = get_item_notes(header_guid, CONST_APPROVER_NOTE, False)
    for sc_hdr_detail in sc_hdr_details:
        sc_header_instance = sc_hdr_detail
        total_val = sc_header_instance['total_value']
        global_variables.GLOBAL_REQUESTER_COMPANY_CODE = sc_header_instance['co_code']
    update_requester_info(sc_header_instance['requester'])
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT,
                                             global_variables.GLOBAL_REQUESTER_OBJECT_ID)
    requesters_currency = global_variables.GLOBAL_REQUESTER_CURRENCY
    is_valid = validate_document_access(sc_header_instance['requester'],
                                        sc_header_instance['created_by'], req, header_guid, access_type)
    if not is_valid:
        return HttpResponseForbidden()
    item_dictionary_list = []
    for sc_items in sc_item_details:
        item_details = {'prod_cat': sc_items.prod_cat, 'value': sc_items.value, 'guid': sc_items.guid}
        item_detail_list.append(item_details)
        item_price_per_unit = sc_items.price
        item_currency = sc_items.currency

        if item_currency is None:
            item_currency = requesters_currency
        if item_currency != requesters_currency:
            item_price_per_unit = convert_currency(item_price_per_unit, str(item_currency), str(requesters_currency))
        item_value_list.append(item_price_per_unit)
        total_value_of_item_converted.append(item_price_per_unit)
    # append eform details to item
    item_dictionary_list = update_eform_scitem(header_guid)
    for item in item_dictionary_list:
        item = update_supplier_uom_for_prod(item)

    for acc_detail in sc_accounting_details:
        gl_acc_num_list.append(acc_detail['gl_acc_num'])
        acc_detail['gl_account_value_desc'] = ACCValueDesc.append_gl_account_value_desc(acc_detail['gl_acc_num'],
                                                                                        global_variables.GLOBAL_REQUESTER_COMPANY_CODE,
                                                                                        global_variables.GLOBAL_REQUESTER_LANGUAGE)

        acc_desc_append = get_acc_desc_append([acc_detail['acc_cat']])
        if acc_desc_append:
            acc_detail['acc_desc'] = acc_desc_append[0]['append_val']
        else:
            acc_detail['acc_desc'] = acc_detail['acc_cat']

        acc_detail['acc_value_desc'] = get_acc_value_and_description_append(acc_detail,
                                                                            acc_detail['acc_cat'],
                                                                            global_variables.GLOBAL_REQUESTER_COMPANY_CODE,
                                                                            global_variables.GLOBAL_REQUESTER_LANGUAGE)

    header_level_gl_acc = get_header_level_gl_acc(gl_acc_num_list)
    header_acc_detail, header_level_acc_guid = get_header_acc_detail(header_guid)
    header_level_addr = get_header_level_addr(header_guid)
    eform_info = get_eform_data(header_guid)
    del_addr = get_del_addr(header_guid)
    pgrp_list = get_pgrp_item(header_guid)
    # highest item guid
    highest_item_guid = get_highest_item_guid(header_guid)

    # requester user name
    sc_header_data, requester_user_name = get_sc_requester_user_name(header_guid)

    requester_full_name = UserData.objects.get(username=requester_user_name, client=global_variables.GLOBAL_CLIENT)
    # Requester Currency
    requester_currency = get_requester_currency(requester_user_name)

    # requester object id
    requester_object_id = get_requester_object_id(requester_user_name)

    ship_to_bill_to_address_instance = ShipToBillToAddress(requester_object_id)
    delivery_addr_list, addr_default, addr_val_desc = get_sc_comp_my_order(requester_object_id)
    product_category = get_prod_cat(req, prod_det=None)
    supplier_data = get_supplier_dropdown()
    GetAttachments.po_attachments = []
    sc_attachments = GetAttachments.get_sc_attachments(header_guid)

    addr_value, addr_default_value = ship_to_bill_to_address_instance.get_default_address_number_and_list()
    delivery_addr_desc = ship_to_bill_to_address_instance.get_all_addresses_with_descriptions(addr_value)

    org_config_acc_desc = ACC_CAT.get_org_model_configured_acc_and_desc(object_id_list,
                                                                        CONST_ACC_CAT)
    client = getClients(req)
    sys_attributes_instance = sys_attributes(client)
    acc_list = org_config_acc_desc['acc_desc_list']
    doc_number_encrypted = encrypt(sc_header_instance['doc_number'])
    context = {'type': type, 'guid': header_guid,
               'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
               'requester': requester_user_name, 'unit': UnitOfMeasures.objects.filter(del_ind=False),
               'product_category': product_category, 'limit_form': UpdateLimitItem(),
               'requesters_currency': requester_currency, 'header_level_gl_acc': header_level_gl_acc,
               'highest_item_guid': highest_item_guid, 'item_detail_list': item_detail_list, 'eform_info': eform_info,
               'hdr_det': sc_hdr_details, 'itm_det': sc_item_details, 'acc_det': sc_accounting_details,
               'requester_first_name': requester_first_name,
               'app_det': sc_approval_data,
               'item_dictionary_list': item_dictionary_list,
               'header_acc_detail': header_acc_detail,
               'header_level_acc_guid': header_level_acc_guid,
               'addr_det': sc_address_data, 'supp_notes': supp_notes, 'int_notes': int_notes, 'appr_notes': appr_notes,
               'header_level_addr': header_level_addr,
               'default_company_code': global_variables.GLOBAL_REQUESTER_COMPANY_CODE,
               'pgrp_list': pgrp_list,
               'acc_list': acc_list,
               'supplier_details': get_supplier_first_second_name(global_variables.GLOBAL_CLIENT),
               'sc_completion_flag': flag,
               'supplier_data': supplier_data, 'del_addr': del_addr, 'delivery_addr_desc': delivery_addr_desc,
               'addr_val_desc': addr_val_desc, 'sc_attachements': sc_attachments,
               'attachment_length': len(sc_attachments), 'receiver_name': requester_user_name,
               'requester_currency': requester_currency, 'sc_header_data': sc_header_data, 'total_val': total_val,
               'inc_nav': True, 'inc_footer': True, 'sc_appr': sc_appr, 'sc_head': sc_header_instance,
               'sc_completion': sc_completion, 'item_count': sc_item_details.count(),
               'total_value_of_item_converted': total_value_of_item_converted, 'country_list': get_country_id(),
               'currency_list': get_currency_list(), 'requester_full_name': requester_full_name,
               'delivery_addr_list': delivery_addr_list, 'doc_number_encrypted': doc_number_encrypted,
               'is_document_detail': True, 'attachment_size': sys_attributes_instance.get_attachment_size(),
               'attachment_extension': sys_attributes_instance.get_attachment_extension(),
               'acct_assignment_category': sys_attributes_instance.get_acct_assignment_category(),
               'edit_address_flag': sys_attributes_instance.get_edit_address(),
               'shipping_address_flag': sys_attributes_instance.get_shipping_address(),
               'country_dropdown': get_country_data()}
    return render(req, template, context)


@login_required
@authorize_view(CONST_MY_ORDER)
def docDetails(req, flag, type, guid, mode, access_type):
    update_user_info(req)
    guid = decrypt(guid)

    sc_header_instance = ScHeader.objects.get(guid=guid)

    # To validate access based on creator and requester
    if flag == 'False':
        is_valid = validate_document_access(sc_header_instance.requester,
                                            sc_header_instance.created_by, req, guid, access_type)
        if not is_valid:
            return HttpResponseForbidden()

    update_user_obj_id_list_info()
    doc_type = type
    doc_guid = guid
    add_default_address_value = []
    header_level_acc = ''
    header_level_acc_desc = ''
    header_level_acc_value_description = ''
    gl_value_description = ''
    header_level_addr = ''
    item_detail_list = []
    total_value_of_item_converted = []
    gl_acc_num_list = []
    header_level_gl_acc = ''
    doc_data = get_doc_details(type, guid)
    hdr_data = doc_data.get('hdr_data', None)
    client = getClients(req)
    sc_header, sc_appr, sc_completion, requester_first_name = get_sc_header_app(hdr_data, client=client)
    itm_data = doc_data.get('itm_data', None)

    requester = sc_header_instance.requester
    base_currency = get_requester_currency(requester)
    update_requester_info(requester)
    check_for_prod_cat = False
    for items in itm_data:
        item_details = {}
        # To validate product category in case of sc completion scenario
        if flag == 'True':
            if not check_for_prod_cat:
                is_validated_for_prod_cat = validate_product_category_id_with_purchaser(sc_header_instance.co_code,
                                                                                        items.prod_cat)
                if is_validated_for_prod_cat:
                    check_for_prod_cat = True
        if flag == 'False':
            item_details = {'prod_cat': items.prod_cat, 'value': items.value}
        item_detail_list.append(item_details)

        add_default_address_value.append(items.ship_to_addr_num)
        price = items.price
        currency = items.currency
        if currency is None:
            currency = get_user_currency(req)
        if currency != base_currency:
            price = convert_currency(price, str(currency), str(base_currency))
        total_value_of_item_converted.append(price)

    if flag == 'True':
        if not check_for_prod_cat:
            return HttpResponseForbidden()

    acc_data = doc_data.get('acc_data', None)
    appr_data = doc_data.get('appr_data', None)
    addr_data = doc_data.get('addr_data', None)
    if flag == 'False':
        for acc_detail in acc_data:
            gl_acc_num_list.append(acc_detail['gl_acc_num'])

        header_level_gl_acc = get_header_level_gl_acc(gl_acc_num_list)

    total_val = sc_header_instance.total_value
    GetAttachments.po_attachments = []
    sc_attachments = GetAttachments.get_sc_attachments(guid)
    item_dictionary_list = update_eform_scitem(guid)
    for items in item_dictionary_list:
        items = update_supplier_uom_for_prod(items)
    # get supplier, internal and approval notes
    supp_notes = get_item_notes(guid, CONST_SUPPLIER_NOTE, True)
    int_notes = get_item_notes(guid, CONST_INTERNAL_NOTE, True)
    appr_notes = get_item_notes(guid, CONST_APPROVER_NOTE, False)

    # get header level acc and addr
    if flag in 'False':
        header_level_acc, header_level_acc_desc, header_level_acc_value_description, gl_value_description \
            = get_header_level_acc(guid)
        header_level_addr = get_header_level_addr(guid)

    eform_info = get_eform_data(guid)
    del_addr = get_del_addr(guid)
    pgrp_list = get_pgrp_item(guid)

    # highest item guid
    highest_item_guid = get_highest_item_guid(guid)

    # get ACC dropdown in  acc pop-up
    acc_value_list, acc_list, acc_value_append, acc_append_desc, default_gl_acc_detail, gl_acc_detail, \
    gl_acc_value_append = get_acc_value_list(guid, flag)

    # requester user name
    sc_header_data, requester_user_name = get_sc_requester_user_name(guid)

    requester_full_name = UserData.objects.get(username=requester_user_name, client=client)
    # Requester Currency
    requester_currency = get_requester_currency(requester_user_name)

    # requester object id
    requester_object_id = get_requester_object_id(requester_user_name)

    ship_to_bill_to_address_instance = ShipToBillToAddress(requester_object_id)
    delivery_addr_list, addr_default, addr_val_desc = get_sc_comp_my_order(requester_object_id)
    product_category = get_prod_cat(req, prod_det=None)
    supplier_data = get_supplier_dropdown()

    if flag == 'True':
        template = 'Doc_Details/sc_completetion_doc_details.html'
    else:
        template = 'Doc_Details/my_order_doc_details.html'

    user_object_id = global_variables.USER_OBJ_ID_LIST
    account_assignment_instance = AccountAssignment(user_object_id)

    addr_value, addr_default_value = ship_to_bill_to_address_instance.get_default_address_number_and_list()
    delivery_addr_desc = ship_to_bill_to_address_instance.get_all_addresses_with_descriptions(addr_value)

    company_code = get_attr_value(client, CONST_CO_CODE, user_object_id, False)

    acc_cat_value, acc_cat_default_value = account_assignment_instance.get_account_assignment_default_and_available_list()
    accounting_data = account_assignment_instance.get_accounting_data(total_val, company_code)
    default_acc = accounting_data['default_acc']
    acc_value_list = accounting_data['acc_value_list']
    default_gl_account = accounting_data['default_gl_account']
    acc_val_desc = ACC_CAT.get_acc_cat_description(acc_cat_value)
    acc_list = ACC_CAT.append_acc_val_desc(acc_val_desc, acc_cat_default_value)

    sc_attachments = GetAttachments.get_sc_attachments(guid)
    print(sc_attachments)

    if acc_cat_value:
        acc_val_desc = ACC_CAT.get_acc_cat_description(acc_cat_value)
        acc_list, acc_default = ACC_CAT.append_acc_val_desc(acc_val_desc, acc_cat_default_value)
        description = AccountingDataDesc

        if acc_cat_default_value == 'CC':
            attr_id = CONST_CT_CTR
            default_acc = get_attr_value(client, attr_id, user_object_id, False)
            ct_ctr_value = get_attr_value(client, attr_id, user_object_id, True)
            acc_value = append_attrlow_desc(client, attr_id, description, default_acc, False)
            acc_value_list = append_attrlow_desc(client, attr_id, description, ct_ctr_value, True)
            default_gl_account = get_gl_account_default_value(client, total_val, company_code, 'CC')

        elif acc_cat_default_value == 'WBS':
            attr_id = CONST_WBS_ELEM
            default_acc = get_attr_value(client, attr_id, user_object_id, False)
            ct_ctr_value = get_attr_value(client, attr_id, user_object_id, True)
            acc_value_list = append_attrlow_desc(client, attr_id, description, ct_ctr_value, True)
            default_gl_account = get_gl_account_default_value(client, total_val, company_code, 'WBS')

        elif acc_cat_default_value == 'AS':
            attr_id = CONST_AS_SET
            default_acc = get_attr_value(client, attr_id, user_object_id, False)
            ct_ctr_value = get_attr_value(client, attr_id, user_object_id, True)
            acc_value_list = append_attrlow_desc(client, attr_id, description, ct_ctr_value, True)
            default_gl_account = get_gl_account_default_value(client, total_val, company_code, 'AS')

        elif acc_cat_default_value == 'OR':
            attr_id = CONST_INT_ORD
            default_acc = get_attr_value(client, attr_id, user_object_id, False)
            ct_ctr_value = get_attr_value(client, attr_id, user_object_id, True)
            acc_value_list = append_attrlow_desc(client, attr_id, description, ct_ctr_value, True)
            default_gl_account = get_gl_account_default_value(client, total_val, company_code, 'OR')

    context = {
        'type': doc_type,
        'guid': doc_guid,
        'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
        'requester': requester,
        'unit': UnitOfMeasures.objects.filter(del_ind=False),
        'product_category': product_category,
        'limit_form': UpdateLimitItem(),
        'requesters_currency': base_currency,
        'header_level_gl_acc': header_level_gl_acc,
        'highest_item_guid': highest_item_guid,
        'item_detail_list': item_detail_list,
        'eform_info': eform_info,
        'item_dictionary_list': item_dictionary_list,
        'hdr_det': hdr_data,  # sc_header
        'itm_det': itm_data,
        'acc_det': acc_data,
        'app_det': appr_data,
        'addr_det': addr_data,
        'supp_notes': supp_notes,
        'int_notes': int_notes,
        'appr_notes': appr_notes,
        'requester_first_name': requester_first_name,
        'header_level_acc': header_level_acc,
        'header_level_acc_desc': header_level_acc_desc,
        'header_level_acc_value_description': header_level_acc_value_description,
        'gl_value_description': gl_value_description,
        'header_level_addr': header_level_addr,
        'pgrp_list': pgrp_list,
        'acc_value_list': acc_value_list,
        'acc_list': acc_list,
        'acc_value_append': acc_value_append,
        'acc_append_desc': acc_append_desc,
        'default_gl_acc_detail': default_gl_acc_detail,
        'gl_acc_detail': gl_acc_detail,
        'gl_acc_value_append': gl_acc_value_append,
        'sc_completion_flag': flag,
        'supplier_data': supplier_data,
        'del_addr': del_addr,
        'delivery_addr_desc': delivery_addr_desc,
        'addr_val_desc': addr_val_desc,
        'sc_attachements': sc_attachments,
        'attachment_length': len(sc_attachments),
        'receiver_name': requester_user_name,
        'requester_currency': requester_currency,
        'sc_header_data': sc_header_data,
        'total_val': total_val,
        'inc_nav': True,
        'inc_footer': True,
        'sc_appr': sc_appr,
        'sc_head': sc_header_instance,
        'sc_completion': sc_completion,
        'item_count': itm_data.count(),
        'default_gl_account': default_gl_account,
        'total_value_of_item_converted': total_value_of_item_converted,
        'country_list': get_country_id(),
        'currency_list': get_currency_list(),
        'requester_full_name': requester_full_name,
        'delivery_addr_list': delivery_addr_list,
        'doc_number_encrypted': encrypt(sc_header_instance.doc_number),
        'is_document_detail': True,
        'supplier_details': get_supplier_first_second_name(global_variables.GLOBAL_CLIENT),
        'sc_attachments': sc_attachments
    }
    sys_attributes_instance = sys_attributes(client)
    context['attachment_size'] = sys_attributes_instance.get_attachment_size()
    context['attachment_extension'] = sys_attributes_instance.get_attachment_extension()
    context['shipping_address_flag'] = sys_attributes_instance.get_shipping_address()
    context['edit_address_flag'] = sys_attributes_instance.get_edit_address()

    return render(req, template, context)


# To download attachments
@login_required
def downloadattach(req):
    path = req.GET['path']
    return download(path)


def get_manager_data(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    sc_app_guid = request.POST.get('sc_appr_guid')
    sc_app = ScApproval.objects.filter(guid=sc_app_guid, client=global_variables.GLOBAL_CLIENT)
    return JsonParser_obj.get_json_from_obj(sc_app)


@transaction.atomic
def update_sc(request):
    """
    :param request:
    :return:
    """
    sc_header_guid = None
    sc_header_instance = None
    shop_assist_status = None
    update_user_info(request)
    if request.method == 'POST':
        update_user_info(request)
        if len(request.POST) > 0:
            if 'update_item_details' in request.POST:
                sc_header_guid = request.POST['header_guid']
                update_item_details = request.POST['update_item_details']
                item_details = json.loads(update_item_details)
                item_guid_list = list(item_details.keys())
                for item_guid in item_guid_list:
                    update_saved_item_instance = UpdateSavedItem(sc_header_guid, item_guid)
                    db_fields = item_details[item_guid]
                    del db_fields['acc_type']
                    del db_fields['acc_value']
                    del db_fields['total_sc_value']
                    update_saved_item_instance.save_to_db_onclick(db_fields)

                sc_total_value = request.POST.get('sc_total_value')
                django_query_instance.django_filter_only_query(ScHeader, {'pk': sc_header_guid}).update(
                    gross_amount=sc_total_value, total_value=sc_total_value
                )

                if 'update_eform_details' in request.POST:
                    print(request.POST['update_eform_details'])

            if 'type' in request.POST:
                doc_type = request.POST['type']
                sc_header_guid = request.POST['header_guid']
                sc_header_instance = django_query_instance.django_get_query(ScHeader, {'guid': sc_header_guid})
                purch_worklist_flag = request.POST['purch_worklist_flag']

                if 'update' in request.POST:
                    update = json.loads(request.POST['update'])
                    json_converted = json.dumps(update)
                    final_data = json.loads(json_converted)

                    for keys in final_data.keys():
                        if keys.startswith('attachment_data') or keys.startswith('attachment_name'):
                            update.pop(keys)
                    update_sc_data(update, sc_header_guid)
                    if purch_worklist_flag == '1':
                        update_purchasing_user(sc_header_guid, CONST_SC_ASSIST_SAVE)

                    ScHeader.objects.update_or_create(guid=sc_header_guid,
                                                      defaults={
                                                          'changed_at': datetime.now(),
                                                          'changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                                      })

                if doc_type == 'submit':
                    # update_approval_status(sc_header_guid)
                    if purch_worklist_flag == '1':
                        update_purchasing_user(sc_header_guid, CONST_SC_ASSIST_SUBMIT)
                    django_query_instance.django_update_query(ScApproval,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'header_guid': sc_header_guid,
                                                               'step_num': '1'},
                                                              {'proc_lvl_sts': CONST_ACTIVE})
                    django_query_instance.django_update_query(ScPotentialApproval,
                                                              {'client': global_variables.GLOBAL_CLIENT,
                                                               'sc_header_guid': sc_header_guid,
                                                               'step_num': '1'},
                                                              {'proc_lvl_sts': CONST_ACTIVE})
                    ScHeader.objects.update_or_create(guid=sc_header_guid,
                                                      defaults={'status': CONST_SC_HEADER_AWAITING_APPROVAL})

                if doc_type == 'order':
                    # not with purchaser work list
                    if purch_worklist_flag == '0':
                        update_approval_status(sc_header_guid)
                        ScHeader.objects.update_or_create(guid=sc_header_guid,
                                                          defaults={
                                                              'status': CONST_SC_HEADER_AWAITING_APPROVAL,
                                                              'ordered_at': datetime.now()
                                                          })

                    else:
                        ScHeader.objects.update_or_create(guid=sc_header_guid,
                                                          defaults={
                                                              'status': CONST_SC_HEADER_INCOMPLETE,
                                                              'ordered_at': datetime.now()
                                                          })
                    manager_detail = request.POST.get('manger_detail')
                    manager_detail = json.dumps(manager_detail)
                    manager_detail = eval(json.loads(manager_detail))
                    if purch_worklist_flag == '0':
                        purch_worklist_flag = False
                    else:
                        purch_worklist_flag = True
                    django_query_instance.django_filter_delete_query(ScPotentialApproval,
                                                                     {'sc_header_guid': sc_header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind': False})
                    django_query_instance.django_filter_delete_query(ScApproval,
                                                                     {'header_guid': sc_header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind': False})

                    if manager_detail[0] != '':
                        if doc_type == 'save':
                            save_sc_approval(manager_detail, sc_header_guid, CONST_SC_HEADER_SAVED, purch_worklist_flag)
                        else:
                            save_sc_approval(manager_detail, sc_header_guid, CONST_SC_HEADER_ORDERED,
                                             purch_worklist_flag)

            if 'is_attachments' in request.POST:
                i = 1
                total_items = int(request.POST['total_items'])
                while i <= total_items:
                    if i > total_items:
                        break
                    if 'item_guid' + str(i) in request.POST:
                        item_guid = request.POST['item_guid' + str(i)]
                        SaveShoppingCart(request,
                                         request.POST,
                                         request.FILES,
                                         request.POST['header_guid'],
                                         'Edit').save_attachments((i - 1), item_guid, i,
                                                                  request.POST['doc_number'])
                    i += 1

    document_detail = {}
    if sc_header_instance:
        document_detail = {'document_number': sc_header_instance.doc_number, 'sc_name': sc_header_instance.description}
    return JsonResponse({'sc_details': True, 'document_detail': document_detail})


def manger_detail(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    item_total_val = []
    data = {}
    quantities = request.POST.getlist('quantity[]')
    price_units = request.POST.getlist('price_unit[]')
    prices = request.POST.getlist('price[]')
    overall_limits = request.POST.getlist('overall_limit[]')
    catalog_qtys = request.POST.getlist('catalog_qty[]')
    call_offs = request.POST.getlist('call_off[]')
    acc_cats = request.POST.getlist('acc_cat[]')
    acc_vals = request.POST.getlist('acc_val[]')
    co_code = request.POST.get('co_code')
    requester_name = request.POST.get('requester_name')
    header_guid = request.POST.get('header_guid')
    item_guid = request.POST.get('item_guid')
    item_price = []
    sc_item = django_query_instance.django_filter_query(ScItem,
                                                        {'header_guid': header_guid,
                                                         'client': global_variables.GLOBAL_CLIENT},
                                                        ['item_num'],
                                                        None)
    for quantity, price_unit, price, overall_limit, catalog_qty, call_off, sc_item_detail in zip(quantities,
                                                                                                 price_units, prices,
                                                                                                 overall_limits,
                                                                                                 catalog_qtys,
                                                                                                 call_offs, sc_item):
        if call_off == CONST_CO01:
            price = calculate_item_price(sc_item_detail['guid'], catalog_qty)
        item_price.append(price)
        item_total = calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit)
        item_total_val.append(item_total)
    total_sc_value = sum(item_total_val)
    item_max_index = item_total_val.index(max(item_total_val))
    acc_cat = acc_cats[item_max_index]
    acc_value = acc_vals[item_max_index]
    if co_code:
        manager_detail, msg_info = get_manger_detail(global_variables.GLOBAL_CLIENT, requester_name, acc_cat,
                                                     total_sc_value, co_code, acc_value,
                                                     global_variables.GLOBAL_USER_CURRENCY)
        if manager_detail:
            manager_detail, approver_id = get_users_first_name(manager_detail)
        data['manager_detail'] = manager_detail
        if msg_info:
            data['msg_info'] = msg_info
    data['total_value'] = total_sc_value
    data['value'] = item_total_val
    data['quantity'] = quantities
    data['catalog_qty'] = catalog_qtys
    data['price_unit'] = price_units
    data['item_price'] = item_price

    return JsonResponse(data)


def trigger_wf(request):
    """
    :param request:
    :return:
    """
    data = {}
    item_detail = JsonParser_obj.get_json_from_req(request)
    data['manager_detail'], data['msg_info'] = get_approver_list(item_detail)

    return JsonResponse(data)


def get_highest_item(request):
    """
    :param request:
    :return:
    """
    data = {}
    item_detail = JsonParser_obj.get_json_from_req(request)
    item_total_value = calculate_item_total_value(item_detail['call_off'], item_detail['quantity'], None,
                                                  item_detail['price_unit'], item_detail['price'],
                                                  item_detail['overall_limit'])
    item_total_value_list = item_detail['item_total_value_list']
    update_item_index = item_detail['update_item_index']
    item_total_value_list.pop(int(update_item_index))
    item_total_value_list.insert(update_item_index, item_total_value)
    data['item_total_value_list'] = type_cast_array_float_to_str(item_total_value_list)
    item_total_value_list = type_cast_array_str_to_float(item_total_value_list)
    data['height_value_index'] = item_total_value_list.index(max(item_total_value_list))
    data['item_total_value'] = item_total_value
    data['total_sc_value'] = sum(item_total_value_list)
    return JsonResponse(data)


@transaction.atomic
def update_delivery_date(request):
    update_user_info(request)
    client = getClients(request)
    org_attr_value_instance = OrgAttributeValues()
    update_info = JsonParser_obj.get_json_from_req(request)
    header_guid = update_info['header_guid']
    sc_requester = django_query_instance.django_get_query(ScHeader, {'guid': header_guid}).requester
    user_object_id = get_object_id_from_username(sc_requester)
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    if request.is_ajax():
        updated_date = {}
        updated_payment_incoterms = {}
        supplier_id = None
        count = 0

        if 'lead_time' in update_info:
            item_guid = update_info['item_guid']
            lead_time = update_info['lead_time']
            supplier_id = update_info['supplier_id']
            django_query_instance.django_filter_only_query(ScItem, {'guid': item_guid}).update(lead_time=lead_time)
            delivery_date = calculate_delivery_date(item_guid, int(lead_time), supplier_id,
                                                    default_calendar_id, client,
                                                    ScItem)
            updated_date[item_guid] = delivery_date
            return JsonResponse({'updated_date': updated_date, 'updated_payment_incoterms': updated_payment_incoterms})

        for item_guid in update_info['delivery_dates']:
            if '-' in item_guid:
                guid = item_guid.split('-')[1]
            else:
                guid = item_guid.split('_')[2]
            item_details = ScItem.objects.get(guid=guid)

            if item_details.call_off not in [CONST_CO02, CONST_CO04]:
                if item_details.call_off == CONST_CO01:
                    supplier_id = item_details.pref_supplier
                else:
                    supplier_id = item_details.supplier_id

            if 'supplier_id' in update_info:
                if item_details.call_off == CONST_CO03:
                    if update_info['supplier_id'][count]:
                        supplier_id = update_info['supplier_id'][count]
                        payterm, incoterm = update_sc_with_supplier_data(supplier_id, item_details.guid)
                        updated_payment_incoterms[item_details.guid] = [payterm, incoterm]

            if item_details.call_off != CONST_CO02 and item_details.call_off != CONST_CO04:
                delivery_date = calculate_delivery_date(guid, int(item_details.lead_time), supplier_id,
                                                        default_calendar_id, client,
                                                        ScItem)
                updated_date[item_guid] = delivery_date
            count += 1

        return JsonResponse({'updated_date': updated_date, 'updated_payment_incoterms': updated_payment_incoterms})


@transaction.atomic
def delete_attachments(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        document_number = request.POST.get('document_number')
        attachment_guid = request.POST.get('attachment_guid')
        item_guid = request.POST.get('item_guid')
        header_guid = request.POST.get('header_guid')

        attachment_data = Attachments.objects.filter(guid=attachment_guid, doc_num=document_number, item_guid=item_guid)
        if attachment_data.exists():
            file_path = Attachments.objects.get(guid=attachment_guid)
            get_file_path = file_path.doc_file
            dir_pa = str(get_file_path).rsplit(str(document_number), 1)[0]
            media_path = settings.MEDIA_ROOT
            attachment_data.delete()
            # File path
            absolute_path = media_path + '\\' + str(get_file_path)
            # Directory path
            dir_path = media_path + '\\' + dir_pa + document_number
            count = Attachments.objects.filter(doc_num=document_number).count()
            if count > 0:
                if os.path.exists(absolute_path):
                    os.remove(absolute_path)
            else:
                shutil.rmtree(dir_path)
        available_attachments = GetAttachments().get_attachments_by_item_number(document_number, item_guid)
        return JsonResponse({'available_attachments': available_attachments}, status=200)


def auto_complete_goods_receiver(request):
    client = getClients(request)
    if 'term' in request.GET:
        qs = UserData.objects.filter(Q(client=client, first_name__icontains=request.GET.get('term')) |
                                     Q(client=client, last_name__icontains=request.GET.get('term')) |
                                     Q(client=client, email__icontains=request.GET.get('term')))

        receiver_names = list()
        for names in qs:
            receiver_names.append(names.first_name + ' ' + names.last_name + ' - ' + names.email)
        print(receiver_names)
        return JsonResponse(receiver_names, safe=False)


def update_user_name(request):
    user_detail = {}
    email_id = request.POST.get('email_id')
    user_detail['user_name'] = get_user_id_by_email_id(email_id)

    return JsonResponse(user_detail, safe=False)


def update_saved_item(request):
    update_user_info(request)
    update_item_detail = JsonParser_obj.get_json_from_req(request)
    sc_header_guid = update_item_detail['sc_header_guid']
    item_guid = update_item_detail['guid']
    update_saved_item_instance = UpdateSavedItem(sc_header_guid, item_guid)

    call_off = update_item_detail['call_off']
    if call_off == CONST_CO04:
        supplier_id = update_item_detail['supplier_id']
        update_item_detail['supplier_id'] = None
        item_details, manager_detail, item_value_converted = update_saved_item_instance.update_limit_item(
            update_item_detail)

        item_details['pref_supplier'] = supplier_id
        return JsonResponse({'total_value': item_value_converted,
                             'manager_detail': manager_detail, 'item_details': item_details}, status=201)

    if call_off == CONST_CO03:
        item_details, total_sc_value, item_with_highest_value, item_delivery_date = update_saved_item_instance.update_pr_item(
            update_item_detail)

        if not item_details:
            return JsonResponse({'error_message': total_sc_value}, status=400)

        return JsonResponse({
            'item_details': item_details, 'total_value': total_sc_value,
            'item_with_highest_value': item_with_highest_value, 'item_delivery_date': item_delivery_date
        }, status=201)

    if call_off == CONST_CO02:
        item_details, eform_details, item_value, item_with_highest_value, total_sc_value = update_saved_item_instance.update_saved_freetext_item(
            update_item_detail)

        if not item_details:
            return JsonResponse({'error_message': total_sc_value}, status=400)

        return JsonResponse({
            'item_details': item_details, 'eform_details': eform_details, 'item_value': item_value,
            'item_with_highest_value': item_with_highest_value, 'total_sc_value': total_sc_value
        }, status=201)

    if call_off == CONST_CO01:
        item_details, item_value, total_sc_value, item_with_highest_value = update_saved_item_instance.update_saved_catalog_item(
            update_item_detail)
        return JsonResponse({
            'item_details': item_details,
            'item_value': item_value,
            'total_value': total_sc_value,
            'item_with_highest_value': item_with_highest_value,
        })
