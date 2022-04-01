from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import CONST_CALENDAR_ID
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import get_requester_currency, get_object_id_from_username
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG124
from eProc_Calendar_Settings.Utilities.calender_settings_generic import calculate_delivery_date
from eProc_Doc_Details.Utilities.details_specific import get_approver_list
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_item_total_value, calculate_item_price
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_by_id
from eProc_Shopping_Cart.context_processors import update_user_obj_id_list_info
from eProc_Shopping_Cart.models import ScItem, ScHeader
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user

django_query_instance = DjangoQueries()


class UpdateSavedItem:
    def __init__(self, sc_header_guid, item_guid):
        self.sc_header_guid = sc_header_guid
        self.sc_header_instance = django_query_instance.django_get_query(ScHeader, {'pk': sc_header_guid})
        self.requester = self.sc_header_instance.requester if self.sc_header_instance is not None else None
        self.requester_currency = get_requester_currency(self.requester)
        self.item_guid = item_guid
        self.get_item_instance = django_query_instance.django_get_query(ScItem, {'guid': self.item_guid})
        self.company_code = self.get_item_instance.comp_code if self.get_item_instance is not None else None
        self.requester_object_id = get_object_id_from_username(self.requester)
        self.org_attr_value_instance = OrgAttributeValues()

    def update_limit_item(self, update_item_detail):
        item_details = {}
        overall_limit = update_item_detail['overall_limit']
        expected_value = update_item_detail['expected_value']
        description = update_item_detail['description']
        prod_cat = update_item_detail['prod_cat']
        currency = update_item_detail['currency']
        supplier_id = update_item_detail['supplier_id']
        follow_up_action = update_item_detail['follow_up_action']

        item_details['cmp_code'] = self.company_code
        prod_cat_desc = get_prod_by_id(prod_cat)

        item_details['overall_limit'] = overall_limit
        item_details['expected_value'] = expected_value
        item_details['description'] = description
        item_details['prod_cat'] = prod_cat
        item_details['prod_cat_desc'] = prod_cat_desc
        item_details['supplier_id'] = supplier_id
        item_details['currency'] = currency

        if follow_up_action == 'Invoice & Confirmation Only':
            item_details['ir_gr_ind'] = True
            item_details['gr_ind'] = False
        else:
            item_details['ir_gr_ind'] = False
            item_details['gr_ind'] = True

        required = update_item_detail['required']
        start_date = update_item_detail['start_date']
        end_date = update_item_detail['end_date']
        item_del_date = update_item_detail['item_del_date']

        if required == 'On':
            item_details['start_date'] = None
            item_details['end_date'] = None
            item_details['item_del_date'] = item_del_date

        if required == 'From':
            item_details['item_del_date'] = None
            item_details['end_date'] = None
            item_details['start_date'] = start_date

        if required == 'Between':
            item_details['item_del_date'] = None
            item_details['end_date'] = end_date
            item_details['start_date'] = start_date

        item_value_converted = convert_currency(overall_limit, currency, self.requester_currency)

        item_details['value'] = item_value_converted
        item_details['acc_type'] = update_item_detail['account_assignment_category']
        item_details['acc_value'] = update_item_detail['account_assignment_value']
        item_details['total_sc_value'] = item_value_converted
        item_details['follow_up_action'] = follow_up_action
        manager_detail = get_approver_list(item_details)

        return item_details, manager_detail, item_value_converted

    def update_pr_item(self, update_item_detail):
        item_details = {}
        item_value_object = update_item_detail['item_value_object']
        call_off = update_item_detail['call_off']
        description = update_item_detail['description']
        ext_product_id = update_item_detail['ext_product_id']
        update_user_obj_id_list_info()
        object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, self.requester_object_id)

        default_calendar_id = self.org_attr_value_instance.get_user_default_attr_value_list_by_attr_id(object_id_list,
                                                                                                       CONST_CALENDAR_ID)[
            1]

        if not ext_product_id:
            ext_product_id = None

        price = update_item_detail['price']
        prod_cat = update_item_detail['prod_cat']
        prod_cat_desc = get_prod_by_id(prod_cat)
        currency = update_item_detail['currency']
        unit = update_item_detail['unit']
        lead_time = update_item_detail['lead_time']
        quantity = update_item_detail['quantity']
        account_assignment_category = update_item_detail['account_assignment_category']
        account_assignment_value = update_item_detail['account_assignment_value']

        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        converted_to_user_currency = convert_currency(item_total_value, currency, self.requester_currency)
        if converted_to_user_currency:
            item_value_object[self.item_guid] = converted_to_user_currency

            for key in item_value_object.keys():
                item_value_object[key] = float(item_value_object[key])

            item_value = list(item_value_object.values())
            total_sc_value = sum(item_value)

            item_details['description'] = description
            item_details['ext_product_id'] = ext_product_id
            item_details['value'] = converted_to_user_currency
            item_details['prod_cat_desc'] = prod_cat_desc
            item_details['unit'] = unit
            item_details['lead_time'] = lead_time
            item_details['cmp_code'] = self.company_code
            item_details['acc_type'] = account_assignment_category
            item_details['acc_value'] = account_assignment_value
            item_details['total_sc_value'] = total_sc_value
            item_details['price'] = price
            item_details['quantity'] = quantity
            item_details['currency'] = currency

            item_delivery_date = calculate_delivery_date(self.item_guid,
                                                         int(lead_time),
                                                         None,
                                                         default_calendar_id,
                                                         global_variables.GLOBAL_CLIENT,
                                                         ScItem)

            item_with_highest_value = max(item_value_object, key=item_value_object.get)
            django_query_instance.django_update_query(ScItem,
                                                      {'guid':update_item_detail['guid'],
                                                       'client':global_variables.GLOBAL_CLIENT,
                                                       'del_ind':False},
                                                      {'price':price,
                                                       'quantity':quantity,
                                                       'value':item_total_value,
                                                       'description':description,
                                                       'prod_cat':update_item_detail['prod_cat'],
                                                       'currency':update_item_detail['currency'],
                                                       'unit':update_item_detail['unit'],
                                                       'lead_time':update_item_detail['lead_time']})
            django_query_instance.django_update_query(ScHeader,
                                                      {'guid': update_item_detail['sc_header_guid'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'total_value': total_sc_value})
            return item_details, total_sc_value, item_with_highest_value, item_delivery_date

        else:
            return False, MSG124, None, None

    def update_saved_freetext_item(self, update_item_detail):
        item_details = {}
        eform_details = {}
        quantity = update_item_detail['quantity']
        price = update_item_detail['price']
        call_off = update_item_detail['call_off']
        currency = self.get_item_instance.currency
        item_value_object = update_item_detail['item_value_object']

        item_details['description'] = update_item_detail['item_name']
        item_details['prod_cat'] = update_item_detail['product_category_id']
        item_details['prod_cat_desc'] = update_item_detail['prod_desc']
        item_details['price'] = price
        item_details['unit'] = update_item_detail['unit']
        item_details['item_del_date'] = update_item_detail['del_date']

        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        converted_to_user_currency = convert_currency(item_total_value, currency, self.requester_currency)
        if converted_to_user_currency:
            item_value_object[self.item_guid] = converted_to_user_currency

            for key in item_value_object.keys():
                item_value_object[key] = float(item_value_object[key])

            item_value = list(item_value_object.values())
            total_sc_value = sum(item_value)

            if update_item_detail['eform']:
                for data in update_item_detail:
                    if 'form_field' in data:
                        eform_details[data] = update_item_detail[data]

            item_with_highest_value = max(item_value_object, key=item_value_object.get)

            return item_details, eform_details, item_value, item_with_highest_value, total_sc_value

        else:
            return False, MSG124, None, None

    def update_saved_catalog_item(self, update_item_detail):
        item_details = {}
        quantity = update_item_detail['quantity']
        price = update_item_detail['price']
        call_off = update_item_detail['call_off']
        guid = update_item_detail['guid']

        sc_item_instance = django_query_instance.django_get_query(ScItem, {'guid': guid})
        currency = sc_item_instance.currency
        item_value_object = update_item_detail['item_value_object']
        price = calculate_item_price(guid, quantity)
        item_total_value = calculate_item_total_value(call_off, quantity, None, 1, price, None)
        converted_to_user_currency = convert_currency(item_total_value, currency, self.requester_currency)
        if converted_to_user_currency:
            item_value_object[self.item_guid] = converted_to_user_currency

        for key in item_value_object.keys():
            item_value_object[key] = float(item_value_object[key])

        item_value = list(item_value_object.values())
        total_sc_value = sum(item_value)
        item_with_highest_value = max(item_value_object, key=item_value_object.get)

        item_details['total_sc_value'] = total_sc_value
        item_details['catalog_qty'] = quantity
        item_details['value'] = item_total_value
        item_details['acc_type'] = ''
        item_details['acc_value'] = ''
        item_details['total_sc_value'] = ''
        item_details['price'] = price
        sc_item_instance.price = price
        sc_item_instance.catalog_qty = quantity
        sc_item_instance.value = item_total_value
        sc_item_instance.save()
        django_query_instance.django_update_query(ScHeader,
                                                  {'guid': sc_item_instance.header_guid,
                                                   'client': global_variables.GLOBAL_CLIENT},
                                                  {'total_value': total_sc_value})

        return item_details, item_total_value, total_sc_value, item_with_highest_value

    def save_to_db_onclick(self, item_details):
        django_query_instance.django_update_query(ScItem, {'guid': self.item_guid}, item_details)
