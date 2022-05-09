from django.db.models import Q

from eProc_Basic.Utilities.constants.constants import CONST_CO01, CONST_CO04, CONST_VARIANT_BASE_PRICING, \
    CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT
from eProc_Basic.Utilities.functions.dictionary_list_functions import rename_dictionary_list_key
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import EformFieldConfig, ProductEformPricing, ProductsDetail
from eProc_Form_Builder.models import EformFieldData
from eProc_Shopping_Cart.models import CartItemDetails, ScItem

django_query_instance = DjangoQueries()


def calculate_item_total_value(call_off, quantity, catalog_qty, price_unit, price, overall_limit):
    """
    :param overall_limit:
    :param call_off:
    :param quantity:
    :param catalog_qty:
    :param price_unit:
    :param price:
    :return:
    """

    if call_off == CONST_CO01:
        if catalog_qty is None:
            catalog_qty = quantity
        value = (float(catalog_qty) * float(price)) / int(price_unit)
        return round(value, 2)

    elif call_off == CONST_CO04:
        value = overall_limit
        return round(value, 2)

    else:
        value = (float(quantity) * float(price)) / int(price_unit)
        return round(value, 2)


def calculate_total_value(username):
    """
    :param username:
    :return:
    """

    total_item_value = []
    cart_items = django_query_instance.django_filter_only_query(CartItemDetails, {
        'username': username, 'client': global_variables.GLOBAL_CLIENT
    })

    for items in cart_items:
        call_off = items.call_off
        if call_off == CONST_CO04:
            total_value = items.overall_limit
            return total_value
        else:
            quantity = items.quantity
            price = items.price
            price_unit = items.price_unit
            value = (float(quantity) * float(price)) / int(price_unit)
            total_item_value.append(value)
    return sum(total_item_value)


def get_product_price_from_eform(form_id):
    """
    gets default price by efrom id
    """
    item_price = get_base_price(form_id)
    if item_price != 0:
        additional_pricing_details = get_additional_default_price_details(form_id)
        item_price = get_item_price(item_price, additional_pricing_details)
    return item_price


def get_base_price(eform_id):
    """

    """
    base_price_value = 0
    base_price_eform_details = django_query_instance.django_get_query(EformFieldConfig,
                                                                      {'eform_id': eform_id,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False,
                                                                       'dropdown_pricetype': CONST_VARIANT_BASE_PRICING},
                                                                      )
    if base_price_eform_details:
        base_price_value = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
            ProductEformPricing,
            {'eform_field_config_guid': base_price_eform_details.eform_field_config_guid,
             'pricing_data_default': True,
             'client': global_variables.GLOBAL_CLIENT}, 'price', None)[0]

    return float(base_price_value)


def get_additional_default_price_details(form_id):
    """

    """
    additional_price_list = []
    additional_price_eform_details = django_query_instance.django_filter_query(EformFieldConfig,
                                                                               {'eform_id': form_id,
                                                                                'client': global_variables.GLOBAL_CLIENT,
                                                                                'del_ind': False,
                                                                                'dropdown_pricetype': CONST_VARIANT_ADDITIONAL_PRICING},
                                                                               None, ['default_eform_field_data',
                                                                                      'eform_field_config_guid'])
    # chage dictionary key from default_eform_field_data to price_data
    additional_price_eform_detail_list = rename_dictionary_list_key('default_eform_field_data', 'pricing_data',
                                                                    additional_price_eform_details)
    # query_list = form_q_query_from_list(additional_price_eform_detail_list)
    for additional_price_eform_detail in additional_price_eform_detail_list:
        additional_price_list.append(django_query_instance.django_filter_query(ProductEformPricing,
                                                                               additional_price_eform_detail,
                                                                               None,
                                                                               ['price', 'operator'])[0])
    return additional_price_list


def get_item_price(base_price, additional_pricing_details):
    """

    """
    item_price = base_price
    for additional_pricing in additional_pricing_details:
        if additional_pricing['operator'] == "PLUS":
            item_price = float(item_price) + float(additional_pricing['price'])

    return item_price


def validate_price1(item_total_value, eform_detail, quantity, eform_id):
    """

    """
    base_price = 0
    validation_error = False
    item_db_total_value = 0
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_BASE_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing, {
                'eform_field_config_guid': eform_data['eform_field_config_guid'],
                'pricing_data': eform_data['eform_field_data']}):
                base_price = \
                    django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                             {'eform_field_config_guid':
                                                                                                  eform_data[
                                                                                                      'eform_field_config_guid'],
                                                                                              'pricing_data':
                                                                                                  eform_data[
                                                                                                      'eform_field_data']},
                                                                                             'price',
                                                                                             None)[0]
                break
    if base_price:
        base_price = check_discount_update_base_price(base_price, quantity, eform_id)
        item_db_total_value = float(base_price)
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_ADDITIONAL_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing, {
                'eform_field_config_guid': eform_data['eform_field_config_guid'],
                'pricing_data': eform_data['eform_field_data']}):
                additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
                    ProductEformPricing,
                    {'eform_field_config_guid': eform_data['eform_field_config_guid'],
                     'pricing_data':
                         eform_data[
                             'eform_field_data']},
                    'price',
                    None)[0]
                item_db_total_value += float(additional_price)
    price = item_db_total_value
    item_db_total_value = float(item_db_total_value) * int(quantity)
    if float(item_db_total_value) != float(item_total_value):
        validation_error = True
    return price, item_db_total_value, validation_error


def validate_price(item_total_value, eform_detail, quantity, eform_id):
    """

    """
    base_price = 0
    validation_error = False
    item_db_total_value = 0
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_BASE_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing,
                                                            {'eform_field_config_guid': eform_data[
                                                                'eform_field_config_guid'],
                                                             'product_eform_pricing_guid': eform_data[
                                                                 'product_eform_pricing_guid']}):
                base_price = \
                    django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                             {'eform_field_config_guid':
                                                                                                  eform_data[
                                                                                                      'eform_field_config_guid'],
                                                                                              'product_eform_pricing_guid':
                                                                                                  eform_data[
                                                                                                      'product_eform_pricing_guid']},
                                                                                             'price',
                                                                                             None)[0]
                break
    if base_price:
        base_price = check_discount_update_base_price(base_price, quantity, eform_id)
        item_db_total_value = float(base_price)
    for eform_data in eform_detail:
        if eform_data['pricing_type'] == CONST_VARIANT_ADDITIONAL_PRICING:
            if django_query_instance.django_existence_check(ProductEformPricing, {
                'eform_field_config_guid': eform_data['eform_field_config_guid'],
                'product_eform_pricing_guid': eform_data['product_eform_pricing_guid']}):
                additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
                    ProductEformPricing,
                    {'eform_field_config_guid': eform_data['eform_field_config_guid'],
                     'product_eform_pricing_guid':
                         eform_data[
                             'product_eform_pricing_guid']},
                    'price',
                    None)[0]
                item_db_total_value += float(additional_price)
    price = item_db_total_value
    item_db_total_value = float(item_db_total_value) * int(quantity)
    if float(item_db_total_value) != float(item_total_value):
        validation_error = True
    return price, item_db_total_value, validation_error


def check_discount_update_base_price(base_price, quantity, eform_id):
    """

    """
    if django_query_instance.django_existence_check(ProductEformPricing,
                                                    {'eform_id': eform_id,
                                                     'pricing_type': CONST_QUANTITY_BASED_DISCOUNT,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'del_ind': False}):
        base_price = calculate_quantity_based_discount(eform_id, quantity, base_price)
    return base_price


def calculate_quantity_based_discount(eform_id, quantity, base_price):
    """

    """
    quantity_price_detail = django_query_instance.django_filter_query(ProductEformPricing,
                                                                      {'eform_id': eform_id,
                                                                       'pricing_type': CONST_QUANTITY_BASED_DISCOUNT,
                                                                       'client': global_variables.GLOBAL_CLIENT,
                                                                       'del_ind': False},
                                                                      ['pricing_data'], ['pricing_data', 'price'])
    range_value_percentage = find_range(quantity_price_detail, quantity)
    if range_value_percentage:
        percentage = 100 - int(range_value_percentage['price'])
        base_price = float(base_price) * percentage / 100
    return base_price


def find_range(quantity_price_details, quantity):
    """

    """
    min_quantity = 0
    range_detail = 0
    quantity = int(quantity)
    for index, quantity_price_detail in enumerate(quantity_price_details):
        if quantity in range(min_quantity, int(quantity_price_detail['pricing_data'])-1):
            if index != 0:
                range_detail = quantity_price_details[index - 1]
            break
        if len(quantity_price_detail) - 1 == index:
            if quantity > int(quantity_price_detail['pricing_data']):
                range_detail = quantity_price_detail
        min_quantity = int(quantity_price_detail['pricing_data'])
    return range_detail


def add_additional_price_to_base_price(base_price, product_eform_pricing_guid_list):
    """

    """
    additional_pricing = []
    if django_query_instance.django_existence_check(ProductEformPricing,
                                                    {'product_eform_pricing_guid__in': product_eform_pricing_guid_list,
                                                     'client': global_variables.GLOBAL_CLIENT,
                                                     'pricing_type': CONST_VARIANT_ADDITIONAL_PRICING,
                                                     'del_ind': False}):
        additional_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                                    {
                                                                                                        'product_eform_pricing_guid__in': product_eform_pricing_guid_list,
                                                                                                        'client': global_variables.GLOBAL_CLIENT,
                                                                                                        'pricing_type': CONST_VARIANT_ADDITIONAL_PRICING,
                                                                                                        'del_ind': False},
                                                                                                    'price', None)

        additional_price = [float(item) for item in additional_price]
        if additional_price:
            additional_pricing = sum(additional_price)
        base_price += additional_pricing

    return base_price


def calculate_item_price(guid, quantity):
    """

    """
    item_price = 0
    eform_id = None
    if CartItemDetails.objects.filter(Q(guid=guid), ~Q(eform_id=None)).exists():
        eform_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                            {'guid': guid},
                                                                                            'eform_id', None)[0]
    elif ScItem.objects.filter(Q(guid=guid), ~Q(eform_id=None)).exists():
        eform_id = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                            {'guid': guid},
                                                                                            'eform_id', None)[0]

    if eform_id:
        pricing_list = [CONST_VARIANT_BASE_PRICING, CONST_VARIANT_ADDITIONAL_PRICING, CONST_QUANTITY_BASED_DISCOUNT]
        if django_query_instance.django_existence_check(EformFieldConfig,
                                                        {'client': global_variables.GLOBAL_CLIENT,
                                                         'del_ind': False,
                                                         'eform_id': eform_id,
                                                         'dropdown_pricetype__in': pricing_list}):
            product_eform_pricing_guid_list = EformFieldData.objects.filter((Q(cart_guid=guid) | Q(item_guid=guid)) &
                                                                            ~Q(product_eform_pricing_guid=None)).values_list(
                'product_eform_pricing_guid',
                flat=True)
            for pricing_guid in product_eform_pricing_guid_list:
                if django_query_instance.django_existence_check(ProductEformPricing,
                                                                {'product_eform_pricing_guid': pricing_guid,
                                                                 'client': global_variables.GLOBAL_CLIENT,
                                                                 'pricing_type': CONST_VARIANT_BASE_PRICING,
                                                                 'del_ind': False}):
                    base_price = \
                        django_query_instance.django_filter_value_list_ordered_by_distinct_query(ProductEformPricing,
                                                                                                 {
                                                                                                     'product_eform_pricing_guid': pricing_guid,
                                                                                                     'client': global_variables.GLOBAL_CLIENT,
                                                                                                     'pricing_type': CONST_VARIANT_BASE_PRICING,
                                                                                                     'del_ind': False},
                                                                                                 'price', None)[0]

            base_price = check_discount_update_base_price(base_price, quantity, eform_id)
            print(base_price)
            item_price = add_additional_price_to_base_price(float(base_price), product_eform_pricing_guid_list)
        else:
            if CartItemDetails.objects.filter(Q(guid=guid), ~Q(eform_id=None)).exists():
                item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                                      {'guid': guid},
                                                                                                      'price', None)[0]
            elif ScItem.objects.filter(Q(guid=guid), ~Q(eform_id=None)).exists():
                item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                      {'guid': guid},
                                                                                                      'price', None)[0]
    else:
        if CartItemDetails.objects.filter(Q(guid=guid)).exists():
            item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(CartItemDetails,
                                                                                                  {'guid': guid},
                                                                                                  'price', None)[0]
        elif ScItem.objects.filter(Q(guid=guid)).exists():
            item_price = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                  {'guid': guid},
                                                                                                  'price', None)[0]
    print(item_price)
    return item_price

#
# def calculate_dynamic_price(eform_id, item_guid):
#     """
#
#     """
#     filter_queue = ~Q(product_eform_pricing_guid=None) & (Q(cart_guid=item_guid) | Q(cart_guid=item_guid))
#     django_query_instance.django_queue_query_value_list(EformFieldData,
#                                                         {'eform_id': eform_id},
#                                                         filter_queue,
#                                                         'product_eform_pricing_guid')
#     calculate_item_price()
