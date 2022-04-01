from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import FieldTypeDesc
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Users.Utilities.user_generic import user_detail_search

django_query_instance = DjangoQueries()
JsonParser_obj = JsonParser()


def delete_user(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    user_data = JsonParser_obj.get_json_from_req(request)
    print(user_data['data'])
    if django_query_instance.django_existence_check(UserData,
                                                        {'email': user_data['data'],
                                                         'del_ind': False}):
        django_query_instance.django_update_query(UserData,
                                                  {'email': user_data['data'],
                                                   'client': global_variables.GLOBAL_CLIENT},
                                                  {'del_ind': True})

    employee_results = django_query_instance.django_filter_only_query(UserData, {
            'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
        })
    response = {'employee_results': employee_results,'success_message': "User deleted"}
    return JsonResponse(response, safe=False)
