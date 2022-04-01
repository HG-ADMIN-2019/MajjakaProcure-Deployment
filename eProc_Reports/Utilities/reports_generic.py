import re
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Configuration.models import Languages,  OrgCompanies
from eProc_Registration.models import UserData
from eProc_Configuration.models.development_data import *

django_query_instance = DjangoQueries()


def get_companylist(req):
    client = getClients(req)

    return django_query_instance.django_filter_value_list_query(OrgCompanies, {'client': client, 'del_ind': False},
                                                                'company_id')


def get_account_assignlist(req):
    return django_query_instance.django_filter_value_list_query(AccountAssignmentCategory, {'del_ind': False},
                                                                'account_assign_cat')


def get_langlist(req):
    return django_query_instance.django_filter_value_list_query(Languages, {'del_ind': False},
                                                                'language_id')


def get_usrid_by_username(username: object, active) -> object:
    if '*' in username and active is not None:
        uname = re.search(r'[a-zA-Z0-9]+', username)
        if username[0] == '*' and username[-1] == '*':
            queryset = django_query_instance.django_filter_only_query(UserData, {'username__icontains': uname.group(0),
                                                                                 'is_active': active})
        elif username[0] == '*':
            queryset = django_query_instance.django_filter_only_query(UserData, {'username__iendswith': uname.group(0),
                                                                                 'is_active': active})
        else:
            queryset = django_query_instance.django_filter_only_query(UserData,
                                                                      {'username__istartswith': uname.group(0),
                                                                       'is_active': active})
    else:
        queryset = django_query_instance.django_filter_only_query(UserData, {'username': username,
                                                                             'is_active': active})

    return queryset
