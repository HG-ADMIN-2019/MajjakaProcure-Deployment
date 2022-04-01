from eProc_Attributes.Utilities.attributes_generic import OrgAttributeValues
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Ship_To_Bill_To_Address.Utilites.ship_to_bill_to_specific import get_shipping_drop_down, Address_desc
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_User_Settings.Utilities.user_settings_specific import UserSettings


class ShipToBillToAddress:

    def __init__(self, user_object_id):
        self.user_object_id = user_object_id
        self.user_object_id_list = get_object_id_list_user(global_variables.GLOBAL_CLIENT, user_object_id)
        self.user_setting = UserSettings()

    def get_default_address_number_and_list(self):
        attr_low_value_list, default_attr_list = OrgAttributeValues.get_user_default_attr_value_list_by_attr_id(self.user_object_id_list, CONST_DEL_ADDR)
        return attr_low_value_list, default_attr_list

    @staticmethod
    def get_default_address_and_available_address_with_description(address_number_list, default_address_number):
        return get_shipping_drop_down(address_number_list, default_address_number)

    @staticmethod
    def get_all_addresses_with_descriptions(address_number_list):
        return Address_desc.get_addr_description(global_variables.GLOBAL_CLIENT, address_number_list,
                                                 CONST_DEL_ADDR, 'D')
