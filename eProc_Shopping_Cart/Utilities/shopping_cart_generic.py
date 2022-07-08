from django.db.models import Q

from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Configuration.models import UnspscCategories, UnspscCategoriesCustDesc
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_po_header_app, get_sc_header_app_wf, \
    get_sc_header_app
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.models import EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_completion_work_flow
from eProc_Shopping_Cart.models import ScItem, ScHeader, ScAccounting, ScPotentialApproval, ScApproval

django_query_instance = DjangoQueries()


# Function to get product category description based on product category Id and display it in drop down
def get_prod_cat(request, prod_det):
    """
    The variable prod_det is used to store product Id  of an item while updating an item in 1st step of shopping cart wizard
    This function is mainly used to display product category in drop down in limit_order, form_builder,
    """
    prod_cat_cust = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {
        'client': global_variables.GLOBAL_CLIENT
    }, 'prod_cat_id')
    prod_cat_cust_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc, {
        'prod_cat_id__in': prod_cat_cust,
        'language_id': global_variables.GLOBAL_USER_LANGUAGE,
        'client': global_variables.GLOBAL_CLIENT
    }, None, ['prod_cat_id', 'category_desc'])
    return prod_cat_cust_desc


# Function to get supplier details based on client and display it in drop down
def get_supplier_details(client, supp_id_up):
    """
    The variable supp_id_up is used to store supplier Id  of an item while updating an item in 1st step of shopping cart wizard
    This function is mainly used to display supplier info in drop down in limit_order, form_builder,
    """
    supp_id = []
    supp_name1 = []
    supp_name2 = []
    suppliers = SupplierMaster.objects.filter(client=client, del_ind=False).values('supplier_id', 'name1', 'name2')

    for supplier_details in suppliers:
        supplier_id = supplier_details['supplier_id']
        supplier_name1 = supplier_details['name1']
        supplier_name2 = supplier_details['name2']
        supp_id.append(supplier_id)
        supp_name1.append(supplier_name1)
        supp_name2.append(supplier_name2)

    # Pop an element from a list to avoid duplicate values in drop down in update functionality
    if supp_id_up is not None:
        for supp_id_item in supp_id:
            if supp_id_item == supp_id_up:
                supp_id_index = supp_id.index(supp_id_up)
                del supp_id[supp_id_index]
                del supp_name1[supp_id_index]
                del supp_name2[supp_id_index]

    supplier_info = zip(supp_id, supp_name1, supp_name2)
    return supplier_info


# Function to get supplier first name and last name based on supplier Id
def get_supp_name_by_id(client, supp_id):
    """
    This function is used to supplier details based on supplier id using in select_supplier.py and html
    """
    supplier = django_query_instance.django_get_query(SupplierMaster, {
        'supplier_id': supp_id, 'client': client, 'del_ind': False
    })
    name1 = supplier.name1
    name2 = supplier.name2
    supp_name = name1 + '          ' + name2
    return supp_name


# Function to get product category details by Id
def get_prod_by_id(prod_id):
    """
    This function is used to get product category description from product Id in update functionality
    """
    description = None
    if prod_id is not None:
        if django_query_instance.django_existence_check(UnspscCategories,
                                                        {'prod_cat_id': prod_id,
                                                         'del_ind': False}):
            if django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                            {'prod_cat_id': prod_id,
                                                             'client': global_variables.GLOBAL_CLIENT,
                                                             'del_ind': False}):
                if django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'del_ind': False,
                                                                 'prod_cat_id': prod_id,
                                                                 'language_id': global_variables.GLOBAL_USER_LANGUAGE}):
                    prod_det = django_query_instance.django_get_query(UnspscCategoriesCustDesc,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'prod_cat_id': prod_id,
                                                                       'language_id': global_variables.GLOBAL_USER_LANGUAGE})
                    description = prod_det.category_desc
                elif django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                                   'del_ind': False,
                                                                   'prod_cat_id': prod_id,
                                                                   'language_id': 'EN'}):
                    prod_det = django_query_instance.django_get_query(UnspscCategoriesCustDesc,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'prod_cat_id': prod_id,
                                                                       'language_id': 'EN'})
                    description = prod_det.category_desc
                else:
                    prod_det = django_query_instance.django_get_query(UnspscCategories,
                                                                      {'del_ind': False,
                                                                       'prod_cat_id': prod_id})
                    description = prod_det.prod_cat_desc
    return description


def get_supplier_first_second_name(client):
    supplier_list = get_registered_org_suppliers(client)
    supp_id = []
    supp_name1 = []
    supp_name2 = []
    for supplier in supplier_list:
        suppliers = django_query_instance.django_get_query(SupplierMaster, {
            'supplier_id': supplier, 'client': client, 'del_ind': False
        })
        supp_id.append(suppliers.supplier_id)
        supp_name1.append(suppliers.name1)
        supp_name2.append(suppliers.name2)

    supplier_info = zip(supp_id, supp_name1, supp_name2)
    return supplier_info


def get_image_url(int_product_id):
    """

    """
    image_url = ''
    if django_query_instance.django_existence_check(ImagesUpload, {
        'client': global_variables.GLOBAL_CLIENT, 'image_id': int_product_id,
        'image_type': CONST_CATALOG_IMAGE_TYPE, 'image_default': True
    }):
        image_url = django_query_instance.django_filter_value_list_query(ImagesUpload, {
            'client': global_variables.GLOBAL_CLIENT, 'image_id': int_product_id,
            'image_type': CONST_CATALOG_IMAGE_TYPE, 'image_default': True
        }, 'image_url')[0]

    return image_url


def update_eform_details_scitem(cart_items):
    """

    """
    filter_queue = Q()
    for cart_item in cart_items:
        if cart_item['call_off'] in [CONST_CATALOG_CALLOFF, CONST_FREETEXT_CALLOFF]:
            if cart_item['eform_id']:
                filter_queue = Q(cart_guid=cart_item['guid']) | Q(item_guid=cart_item['guid'])
                if django_query_instance.django_queue_existence_check(EformFieldData,
                                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      filter_queue):
                    cart_item['eform_data'] = django_query_instance.django_queue_query(EformFieldData,
                                                                                       {
                                                                                           'client': global_variables.GLOBAL_CLIENT,
                                                                                           'del_ind': False},
                                                                                       filter_queue,
                                                                                       None,
                                                                                       None)
    return cart_items


def get_highest_acc_detail(header_guid):
    """

    """
    previous_item_highest_value = django_query_instance.django_filter_only_query(ScItem, {
        'header_guid': django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
    }).order_by('-value')[0]

    highest_item_accounting_data = django_query_instance.django_get_query(ScAccounting, {
        'item_guid': previous_item_highest_value.guid
    })

    account_assignment_category = highest_item_accounting_data.acc_cat
    if account_assignment_category == 'CC':
        account_assignment_value = highest_item_accounting_data.cost_center

    elif account_assignment_category == 'AS':
        account_assignment_value = highest_item_accounting_data.asset_number

    elif account_assignment_category == 'OR':
        account_assignment_value = highest_item_accounting_data.internal_order

    else:
        account_assignment_value = highest_item_accounting_data.wbs_ele
    return account_assignment_category, account_assignment_value


def delete_approver_detail(header_guid):
    """

    """

    if django_query_instance.django_existence_check(ScPotentialApproval, {'sc_header_guid': header_guid,
                                                                          'client': global_variables.GLOBAL_CLIENT}):
        django_query_instance.django_filter_delete_query(ScPotentialApproval, {'sc_header_guid': header_guid,
                                                                               'client': global_variables.GLOBAL_CLIENT})
    if django_query_instance.django_existence_check(ScApproval, {'header_guid': header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT}):
        django_query_instance.django_filter_delete_query(ScApproval, {'header_guid': header_guid,
                                                                      'client': global_variables.GLOBAL_CLIENT})


def get_price_discount_tax(price, base_price, additional_price, tax, discount_percentage, quantity):
    """

    """
    actual_price = float(base_price) + float(additional_price)
    discount_value = float(base_price) * float(discount_percentage / 100) * int(quantity)
    if tax:
        if not tax['sgst']:
            tax['sgst'] = 0
        if not tax['cgst']:
            tax['cgst'] = 0
        if not tax['vat']:
            tax['vat'] = 0
        sgst = float(price) * (float(tax['sgst']) / 100) * int(quantity)
        cgst = float(price) * (float(tax['cgst']) / 100) * int(quantity)
        vat = float(price) * (float(tax['vat']) / 100) * int(quantity)
        tax_value = sgst + cgst + vat
        gross_price = float(price) + float(
            (float(price) * (float(tax['sgst']) / 100)) + (float(price) * (float(tax['cgst']) / 100)) + (
                    float(price) * (float(tax['vat']) / 100)))
    else:
        tax_value = 0
        gross_price = price
    return actual_price, discount_value, tax_value, gross_price


def get_total_price_details(item_details, user_currency):
    """

    """
    actual_price_list = []
    discount_value_list = []
    tax_value_list = []
    price_details = {}
    for items in item_details:
        if items['currency'] != user_currency:
            actual_price_list.append(
                convert_currency(float(items['actual_price']) * items['quantity'], str(items['currency']),
                                 str(user_currency)))
            discount_value_list.append(
                convert_currency(items['discount_value'], str(items['currency']), str(user_currency)))
            tax_value_list.append(convert_currency(items['tax_value'], str(items['currency']), str(user_currency)))
            # gross_price_list.append(convert_currency(float(items['gross_price'])*items['quantity'], str(items['currency']), str(user_currency)))
        else:
            actual_price_list.append(float(items['actual_price']) * items['quantity'])
            discount_value_list.append(items['discount_value'])
            tax_value_list.append(items['tax_value'])
            # gross_price_list.append(float(items['gross_price'])*items['quantity'])
    actual_price = round(sum(actual_price_list), 2)
    discount_value = round(sum(discount_value_list), 2)
    tax_value = round(sum(tax_value_list), 2)
    price_details = {'actual_price': format(actual_price, '.2f'),
                     'discount_value': format(discount_value, '.2f'),
                     'tax_value': format(tax_value, '.2f')}
    return price_details


def get_total_value(sc_item_details, requester_currency):
    """

    """
    value = []
    for sc_item_detail in sc_item_details:
        total_item_value = calculate_item_total_value(sc_item_detail['call_off'], sc_item_detail['quantity'],
                                                      sc_item_detail['quantity'], sc_item_detail['price_unit'],
                                                      sc_item_detail['price'], sc_item_detail['overall_limit'])
        value.append(convert_currency(total_item_value, str(sc_item_detail['currency']), str(requester_currency)))
    if value:
        sc_total_value = round(sum(value), 2)
    else:
        sc_total_value = 0
    return sc_total_value


def get_SC_details_email(sc_header_guid):
    """

    """
    po_header_details = django_query_instance.django_filter_query(ScHeader,
                                                                  {'guid': sc_header_guid,
                                                                   'client': global_variables.GLOBAL_CLIENT},
                                                                  None,
                                                                  None)

    sc_item_details = django_query_instance.django_filter_query(ScItem,
                                                                {'header_guid': sc_header_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT},
                                                                None,
                                                                None)
    for po_header_detail in sc_item_details:
        po_header_detail['supplier_description'] = django_query_instance.django_filter_value_list_query(SupplierMaster,
                                                                                                        {
                                                                                                            'client': global_variables.GLOBAL_CLIENT,
                                                                                                            'supplier_id':
                                                                                                                po_header_detail[
                                                                                                                    'supplier_id']},
                                                                                                        'name1')[0]
    po_item_guid_list = dictionary_key_to_list(po_header_details, 'guid')

    sc_accounting_details = django_query_instance.django_filter_query(ScAccounting,
                                                                      {'header_guid__in': po_item_guid_list,
                                                                       'client': global_variables.GLOBAL_CLIENT},
                                                                      None,
                                                                      None)

    po_header_details, po_approver_details, sc_completion, requester_first_name = get_sc_header_app(po_header_details, global_variables.GLOBAL_CLIENT)

    context = {'po_header_details': po_header_details,
               'sc_item_details': sc_item_details,
               'sc_accounting_details': sc_accounting_details,
               'po_approver_details': po_approver_details,
               'sc_completion': sc_completion,
               'requester_first_name': requester_first_name,

               }
    return context


def get_acc_detail(header_guid):
    """

    """
    item_accounting_data = django_query_instance.django_get_query(ScAccounting, {
        'guid': header_guid
    })

    account_assignment_category = item_accounting_data.acc_cat
    if account_assignment_category == 'CC':
        account_assignment_value = item_accounting_data.cost_center

    elif account_assignment_category == 'AS':
        account_assignment_value = item_accounting_data.asset_number

    elif account_assignment_category == 'OR':
        account_assignment_value = item_accounting_data.internal_order

    else:
        account_assignment_value = item_accounting_data.wbs_ele
    return account_assignment_value
