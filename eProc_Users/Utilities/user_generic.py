from django.db.models import Q
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Registration.models import UserData


def user_detail_search(**kwargs):
    """

    """
    search_query = {}
    client = global_variables.GLOBAL_CLIENT
    username_query = Q()
    first_name_query = Q()
    last_name_query = Q()
    email_query = Q()
    user_type_query = Q()
    employee_id_query = Q()
    pwd_locked_query = Q()
    user_locked_query = Q()
    instance = UserData()
    for key, value in kwargs.items():
        value_list = []
        if value:
            # if key == 'supplier_id':
            #     supp_query = get_supplier_id(value)
            # if key == 'prod_cat_id':
            #     product_category_query = get_product_category_id(value)
            if key == 'username':
                if '*' not in value:
                    value_list = [value]
                username_query = django_q_query(value, value_list, 'username')
            if key == 'first_name':
                if '*' not in value:
                    value_list = [value]
                first_name_query = django_q_query(value, value_list, 'first_name')
            if key == 'last_name':
                if '*' not in value:
                    value_list = [value]
                last_name_query = django_q_query(value, value_list, 'last_name')
            if key == 'email':
                if '*' not in value:
                    value_list = [value]
                email_query = django_q_query(value, value_list, 'email')
            if key == 'user_type':
                if '*' not in value:
                    value_list = [value]
                user_type_query = django_q_query(value, value_list, 'user_type')
            if key == 'employee_id':
                if '*' not in value:
                    value_list = [value]
                employee_id_query = django_q_query(value, value_list, 'employee_id')
            if key == 'pwd_locked':
                value = '1'
                value_list = '1'
                pwd_locked_query = django_q_query(value, value_list, 'pwd_locked')
            if key == 'user_locked':
                value = '1'
                value_list = '1'
                user_locked_query = django_q_query(value, value_list, 'user_locked')

    user_details_query = list(instance.get_user_details_by_fields(client,
                                                                  instance,
                                                                  username_query,
                                                                  first_name_query,
                                                                  last_name_query,
                                                                  email_query,
                                                                  user_type_query,
                                                                  employee_id_query,
                                                                  pwd_locked_query,
                                                                  user_locked_query,
                                                                  ))
    # user_details_query = list(
    #     UserData.objects.filter(username_query, email_query, client=client,
    #                             del_ind=False
    #                             ).values().order_by('username'))
    # print(user_details_query)
    return user_details_query
