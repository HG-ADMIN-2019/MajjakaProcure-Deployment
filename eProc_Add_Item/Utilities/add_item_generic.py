from eProc_Basic.Utilities.constants.constants import CONST_CO01
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_price, calculate_item_total_value
from eProc_Shopping_Cart.models import ScItem, ScHeader

django_query_instance = DjangoQueries()


def exists_update_sc_item(header_guid,cart_item_detail,ui_quantity):
    """

    """
    db_quantity = cart_item_detail['catalog_qty']
    quantity = int(cart_item_detail['catalog_qty']) + int(ui_quantity)
    item_price = calculate_item_price(cart_item_detail['guid'], quantity)
    price_total_value = calculate_item_total_value(CONST_CO01, quantity,
                                                   quantity, 1,
                                                   item_price, overall_limit=None)
    django_query_instance.django_update_query(ScItem,
                                              {'guid': cart_item_detail['guid'],
                                               'client': global_variables.GLOBAL_CLIENT,
                                               'del_ind': False},
                                              {'catalog_qty': quantity,
                                               'value': price_total_value,
                                               'price':item_price})
    sc_item_value_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ScItem,
                                                                                                  {
                                                                                                      'client': global_variables.GLOBAL_CLIENT,
                                                                                                      'header_guid': header_guid},
                                                                                                  'value', None)
    total_value = sum(sc_item_value_list)
    django_query_instance.django_update_query(ScHeader,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'guid': header_guid}, {'total_value': total_value})
    return True