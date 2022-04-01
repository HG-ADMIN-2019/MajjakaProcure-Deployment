# Utility functions for search functionality
# Utils is a collection of small functions and classes which make common patterns shorter and easier.

import os

from django.http import Http404
from Majjaka_eProcure import settings
from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_SC_HEADER_APPROVED, CONST_COMPLETED, CONST_SC_APPR_APPROVED, \
    CONST_SC_HEADER_AWAITING_APPROVAL, CONST_ACTIVE, CONST_AUTO, CONST_INITIATED, CONST_SC_APPR_OPEN, CONST_CO03, \
    CONST_CALENDAR_ID, CONST_CO01
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_object_id_from_username
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Configuration.models import ImagesUpload
from eProc_Notes_Attachments.models import Attachments, Notes
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value
from eProc_Purchase_Order.models.purchase_order import PoHeader, PoItem, PoAccounting, PoApproval

# Importing  the models from m_database app
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import update_eform_details_scitem, get_image_url
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_login_user_spend_limit

from eProc_Shopping_Cart.models import *
import datetime
django_query_instance = DjangoQueries()
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user


# Get Item, Accounting and Approval details from header guid
def get_doc_details(type, hdr_guid):
    if type == 'SC':
        hdr_obj = ScHeader()
        itm_obj = ScItem()
        acc_obj = ScAccounting()
        appr_obj = ScApproval()
        addr_obj = ScAddresses()
    elif type == 'PO':
        hdr_obj = PoHeader()
        itm_obj = PoItem()
        acc_obj = PoAccounting()
        appr_obj = PoApproval()
    else:
        raise Http404
    hdr_data = hdr_obj.get_hdr_data_by_guid(hdr_guid)
    itm_data = itm_obj.get_itms_by_guid(hdr_guid)
    itm_guids = []
    for item in itm_data:
        itm_guids.append(getattr(item, 'guid'))
    acc_data = acc_obj.get_acc_data_by_guid(itm_guids)
    appr_data = appr_obj.get_apprs_by_guid(hdr_guid)
    addr_data = addr_obj.get_addr_by_guid(itm_guids)
    return {'hdr_data': hdr_data, 'itm_data': itm_data, 'acc_data': acc_data, 'appr_data': appr_data,
            'addr_data': addr_data}


# Get attachments by path
class GetAttachments:
    po_attachments = []

    @staticmethod
    def get_sc_attachments(guid):
        attachment_data = []
        if Attachments.objects.filter(header_guid=guid).exists():
            attachment_file_path = Attachments.objects.filter(header_guid=guid).order_by('item_num')
            for attachments in attachment_file_path:
                item_guid = attachments.item_guid
                file_path = str(attachments.doc_file)
                split_file_path = file_path.split('/')
                file_path = '/'.join(split_file_path[:-1])
                file_path = 'media/' + file_path
                GetAttachments.get_all_files(file_path, item_guid)
                file_name = split_file_path[6]
                attachment_dict = {
                    'attachment_guid': attachments.guid,
                    'item_guid': attachments.item_guid,
                    'file_name': file_name,
                    'file_path': file_path + '/' + file_name,
                    'attachment_name': attachments.title,
                    'type': attachments.attach_type_flag,
                    'item_num': attachments.item_num,
                }
                attachment_data.append(attachment_dict)
        return attachment_data

    @staticmethod
    def get_attachments_by_item_number(document_number, item_guid):
        available_attachments = Attachments.objects.filter(doc_num=document_number, item_guid=item_guid,
                                                           del_ind=False).order_by('item_num')
        attachment_data = []
        if available_attachments:
            attachment_file_path = available_attachments
            for attachments in attachment_file_path:
                item_guid = attachments.item_guid
                file_path = str(attachments.doc_file)
                split_file_path = file_path.split('/')
                file_path = '/'.join(split_file_path[:-1])
                file_path = 'media/' + file_path
                GetAttachments.get_all_files(file_path, item_guid)
                file_name = split_file_path[6]
                attachment_dict = {
                    'attachment_guid': attachments.guid,
                    'item_guid': attachments.item_guid,
                    'file_name': file_name,
                    'file_path': file_path + '/' + file_name,
                    'attachment_name': attachments.title,
                    'type': attachments.attach_type_flag,
                    'item_num': attachments.item_num,
                }
                attachment_data.append(attachment_dict)
        return attachment_data

    def get_attachments(self, req, hdr_guid):  # Get attachments by PO header guid
        client = getClients(req)  # To get logged in users client
        self.po_attachments = []
        hdr_obj = PoHeader()
        objid = hdr_obj.get_objid_by_guid(hdr_guid)
        item_guid = ''
        attach_dir = settings.ATTACH_PATH + '/' + client + '/Attachments'  # Get attachments path by settings.py file
        attach_file_path = None
        if os.path.exists(attach_dir):
            dir_list = os.listdir(attach_dir)
            for dir in dir_list:
                if attach_file_path is None:
                    tmp_file = attach_dir + '/' + dir
                    if os.path.exists(tmp_file):
                        sub_list = os.listdir(tmp_file)
                        for subfile in sub_list:
                            sub_path = tmp_file + '/' + subfile
                            if os.path.exists(sub_path) and subfile == objid:
                                attach_file_path = sub_path
                                break
                else:
                    break
        if attach_file_path is not None:
            self.get_all_files(attach_file_path, item_guid)
        return self.po_attachments

    # To get all files inside the attachments and popdf's
    @staticmethod
    def get_all_files(path, item_guid):
        if os.path.exists(path):
            if os.path.isfile(path):
                path = path.replace('&', '%26')
                return GetAttachments.po_attachments.append((path, os.path.basename(path), item_guid))
            elif os.path.isdir(path):
                for subfile in os.listdir(path):
                    GetAttachments.get_all_files(path + '/' + subfile, item_guid)

    # Get POPDF files by Header guid
    def get_popdf(self, req, hdr_guid):
        file_list = []
        objid = PoHeader.get_objid_by_guid(hdr_guid)
        client = getClients(req)  # To get logged in users client
        # POPODF path based on user client
        pdf_path = settings.ATTACH_PATH + '/' + client + '/POPDF/PO_' + objid  # Get POPDF path by settings.py
        if os.path.exists(pdf_path):
            directory = os.listdir(pdf_path)
            for files in directory:
                fname = pdf_path + '/' + files
                fname = fname.replace('&', '%26')
                pdf = (fname, files)
                file_list.append(pdf)
                return file_list


def update_sc_data(sc_data, scheader_guid):
    """

    :param sc_data:
    :param scheader_guid:
    :return:
    """
    # update ScHeader change
    hdr_obj = ScHeader
    save_update_sc(sc_data, hdr_obj, 'ScHeader', 'guid', scheader_guid)

    # update ScAccounting change
    hdr_obj = ScAccounting
    save_update_sc(sc_data, hdr_obj, 'ScAccounting', 'guid', scheader_guid)

    # update ScAddresses change
    hdr_obj = ScAddresses
    save_update_sc(sc_data, hdr_obj, 'ScAddresses', 'guid', scheader_guid)

    # update Notes change
    hdr_obj = Notes
    save_update_sc(sc_data, hdr_obj, 'Notes', 'guid', scheader_guid)

    # update ScItem change
    hdr_obj = ScItem
    save_update_sc(sc_data, hdr_obj, 'ScItem', 'guid', scheader_guid)


def save_update_sc(sc_data, db_table_name, db_name, pk_value, header_guid):
    scitem_dictionary = []
    org_attr_value_instance = OrgAttributeValues()
    sc_header_instance = ScHeader.objects.get(guid=header_guid)
    sc_requester = sc_header_instance.requester
    user_object_id = get_object_id_from_username(sc_requester)
    object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
    default_calendar_id = org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                              CONST_CALENDAR_ID)[1]
    for field, field_value in sc_data.items():
        update_dict = {}
        flag = 0
        match = re.search('(\w+)-(\w+)-(\w+)', field)
        if match is not None:
            if db_name == match.group(1):
                if not hasattr(update_dict, pk_value):
                    update_dict[pk_value] = match.group(3)
                    update_dict[match.group(2)] = field_value
                for val in scitem_dictionary:
                    if val[pk_value] == update_dict[pk_value]:
                        val.update(update_dict)
                        flag = 1
                if not scitem_dictionary or not flag:
                    scitem_dictionary.append(update_dict)

    item_guid = {}

    for scitem in scitem_dictionary:
        item_guid[pk_value] = str(list(scitem.values())[0])
        if db_name == 'ScItem':
            item_instance = ScItem.objects.get(guid=item_guid[pk_value])
            # if item_instance.call_off == CONST_CO03:
            #     calculate_delivery_date(item_guid[pk_value], int(item_instance.lead_time), scitem['supplier_id'],
            #                             default_calendar_id, global_variables.GLOBAL_CLIENT, ScItem)

            quantity, catalog_qty, price_unit, price, overall_limit = check_key_exist(scitem, item_instance)
            item_total_value = calculate_item_total_value(item_instance.call_off, quantity, catalog_qty, price_unit,
                                                          price, overall_limit)
            sc_header_instance.total_value = round(float(sc_header_instance.total_value) - float(item_instance.value) + float(
                item_total_value), 2)
            sc_header_instance.save()
            scitem['value'] = item_total_value
        if db_name == 'ScAddresses':
            item_guid['address_type'] = 'D'
        save_sc_item_details_to_db(db_table_name, scitem, **item_guid)


def update_approval_status(scheader_guid):
    """

    :param scheader_guid:
    :return:
    """
    sc_approval = ScApproval.objects.filter(header_guid=scheader_guid).order_by('-step_num').first()
    received_time, proc_time = get_received_proc_time(sc_approval)
    proc_lvl_sts, app_sts = get_proc_appr_level_status(sc_approval)
    django_query_instance.django_update_query(ScApproval,
                                              {'header_guid':scheader_guid,
                                               'client':global_variables.GLOBAL_CLIENT,
                                               'del_ind':False},
                                              {'received_time':received_time,
                                               'proc_time':proc_time,
                                               'proc_lvl_sts':proc_lvl_sts,
                                               'app_sts':app_sts})

    # sc_approval.received_time = received_time
    # sc_approval.proc_time = proc_time
    # sc_approval.proc_lvl_sts = proc_lvl_sts
    # sc_approval.app_sts = app_sts
    # sc_approval.save()


def get_received_proc_time(sc_approval):
    """

    :param sc_approval:
    :return:
    """
    received_time = None
    proc_time = None
    if sc_approval.app_id == CONST_AUTO:
        received_time = datetime.datetime.now()
        proc_time = datetime.datetime.now()
    elif int(sc_approval.step_num) == 1:
        received_time = datetime.datetime.now()
    return received_time, proc_time


def get_proc_appr_level_status(sc_approval):
    """

    :param sc_approval:
    :return:
    """
    proc_lvl_sts = CONST_INITIATED
    app_sts = CONST_SC_APPR_OPEN
    if int(sc_approval.step_num) == 1:
        proc_lvl_sts = CONST_ACTIVE
    if sc_approval.app_id == CONST_AUTO:
        proc_lvl_sts = CONST_COMPLETED
        app_sts = CONST_SC_APPR_APPROVED
    return proc_lvl_sts, app_sts


def check_key_exist(scitem, item_instance):
    """

    :param scitem:
    :param item_instance:
    :return:
    """
    if checkKey(scitem, 'quantity'):
        quantity = scitem['quantity']
    else:
        quantity = item_instance.quantity

    if checkKey(scitem, 'catalog_qty'):
        catalog_qty = scitem['catalog_qty']
    else:
        catalog_qty = item_instance.catalog_qty

    if checkKey(scitem, 'price_unit'):
        price_unit = scitem['price_unit']
    else:
        price_unit = item_instance.price_unit

    if checkKey(scitem, 'price'):
        price = scitem['price']
    else:
        price = item_instance.price

    if checkKey(scitem, 'overall_limit'):
        overall_limit = scitem['overall_limit']
    else:
        overall_limit = item_instance.overall_limit

    return quantity, catalog_qty, price_unit, price, overall_limit


def save_sc_item_details_to_db(db_table_name, sc_item_details, **kwargs):
    db_table_name.objects.update_or_create(**kwargs, defaults=sc_item_details)


def update_scheader_approval_status(scheader_guid):
    """

    :param scheader_guid:
    :return:
    """
    sc_header_instant = ScHeader.objects.get(guid=scheader_guid)
    login_user_spend_limit, sl_code_id = get_login_user_spend_limit(sc_header_instant.co_code,
                                                                    global_variables.GLOBAL_CLIENT,
                                                                    sc_header_instant.requester)
    if float(sc_header_instant.total_value) < float(login_user_spend_limit):
        ScHeader.objects.filter(guid=scheader_guid).update(status=CONST_SC_HEADER_APPROVED)
        ScApproval.objects.filter(header_guid=scheader_guid).update(proc_lvl_sts=CONST_COMPLETED,
                                                                    app_sts=CONST_SC_APPR_APPROVED,
                                                                    received_time=datetime.datetime.now(),
                                                                    proc_time=datetime.datetime.now())
    else:
        ScHeader.objects.filter(guid=scheader_guid).update(status=CONST_SC_HEADER_AWAITING_APPROVAL)
        ScApproval.objects.filter(header_guid=scheader_guid).update(proc_lvl_sts=CONST_ACTIVE,
                                                                    received_time=datetime.datetime.now())


def update_eform_scitem(header_guid):
    """

    """
    item_dictionary_list = django_query_instance.django_filter_query(ScItem,
                                                                     {'header_guid': header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                      'del_ind':False},
                                                                     ['item_num'], None)
    item_dictionary_list = update_eform_details_scitem(item_dictionary_list)
    for item_dictionary in item_dictionary_list:
        if item_dictionary['call_off'] == CONST_CO01:
            item_dictionary['image_url'] = get_image_url(item_dictionary['int_prod_id'])
        else:
            item_dictionary['image_url'] = ''
    return item_dictionary_list
