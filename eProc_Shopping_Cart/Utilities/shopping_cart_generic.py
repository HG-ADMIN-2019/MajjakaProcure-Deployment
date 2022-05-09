from django.db.models import Q

from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Configuration.models import UnspscCategories, UnspscCategoriesCustDesc
from eProc_Form_Builder.models import EformFieldData
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
    if prod_id is not None:
        prod_cat = django_query_instance.django_existence_check(UnspscCategories, {
            'prod_cat_id': prod_id, 'del_ind': False
        })
        if prod_cat:
            prod_det = django_query_instance.django_get_query(UnspscCategoriesCustDesc, {
                'client': global_variables.GLOBAL_CLIENT, 'del_ind': False,
                'prod_cat_id': django_query_instance.django_get_query(UnspscCategories, {'prod_cat_id': prod_id}),
                'language_id': global_variables.GLOBAL_USER_LANGUAGE
            })

            return prod_det.category_desc


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
        if cart_item['call_off'] in [CONST_CO01, CONST_CO02]:
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
