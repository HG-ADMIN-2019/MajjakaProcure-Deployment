from eProc_Attributes.Utilities.attributes_specific import get_attr_value_list, get_extended_att_list, \
    save_extended_responsibility
from eProc_Basic.Utilities.constants.constants import CONST_PROD_CAT
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()


def extended_attr(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    # get requested object id from UI
    object_id = request.POST.get('obj_id')
    attr_value_list = get_extended_att_list(client, object_id, CONST_PROD_CAT)
    return JsonParser_obj.get_json_from_obj(attr_value_list)


def save_ext_attr(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    save_ext_data = JsonParser_obj.get_json_from_req(request)
    client = global_variables.GLOBAL_CLIENT
    attr_object_id = save_ext_data[0]['obj_id']
    # save extend attributes to OrgAttributesLevel db table
    save_extended_responsibility(save_ext_data)
    attr_value_list = get_attr_value_list(client, attr_object_id)
    return JsonParser_obj.get_json_from_obj(attr_value_list)
