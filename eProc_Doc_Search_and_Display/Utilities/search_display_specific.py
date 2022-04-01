from datetime import date, timedelta

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import requester_field_info
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgPGroup
from eProc_Org_Model.models import OrgModel
from eProc_Shopping_Cart.models import *
from eProc_Registration.models import UserData
from eProc_Basic.Utilities.constants.constants import *
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import get_completion_work_flow
from eProc_Shopping_Cart.models import ScApproval, ScItem
from eProc_User_Settings.Utilities.user_settings_generic import get_object_id_list_user
from eProc_User_Settings.Utilities.user_settings_specific import DocSearch
import datetime

django_query_instance = DjangoQueries()


def get_my_order_default(client, login_user_obj_id):
    """

    :return:
    """
    sc_po = ''
    object_id_list = get_object_id_list_user(client, login_user_obj_id)

    my_order_default_val = django_query_instance.django_filter_value_list_query(OrgAttributesLevel, {
        'object_id__in': object_id_list,
        'client': client,
        'attr_level_default': True,
        'attribute_id': CONST_DEF_DOC_SEARCH
    }, 'low')

    if my_order_default_val:
        my_order_default = my_order_default_val
        sc_po_default = DocSearch.get_doc_search_description(my_order_default)
        sc_po = sc_po_default[0]['document_type_desc']

    return sc_po


def get_sc_header_app(result, client):
    """
    :param client:
    :param result:
    :return:
    """

    sc_header = []
    sc_appr = []
    cmp_code = []
    sc_completion = []
    requester_first_name = ''
    for sc_header_guid in result:

        # convert timestamp to locale date
        created_at_date = sc_header_guid['created_at']
        sc_header_guid['created_at'] = created_at_date.strftime("%d %B %Y ")
        guid_completion = []
        prod_cat_list = []
        call_off_list = []

        sc_approval = django_query_instance.django_filter_query(ScApproval,
                                                                {'header_guid': sc_header_guid['guid'],
                                                                 'client': client},
                                                                ['step_num'], None)
        for sc_app in sc_approval:
            if django_query_instance.django_filter_count_query(ScPotentialApproval,
                                                               {'sc_approval_guid': sc_app['guid']}) > 1:
                sc_app['app_id'] = CONST_MULTIPLE
            else:
                sc_app['app_id'] = django_query_instance.django_filter_value_list_query(ScPotentialApproval,
                                                                                        {'sc_approval_guid':
                                                                                             sc_app['guid']},
                                                                                        'app_id')[0]

        scitems = django_query_instance.django_filter_only_query(ScItem, {'header_guid': sc_header_guid['guid'],
                                                                          'client': client})
        for scitems in scitems:
            prod_cat_list.append(scitems.prod_cat)
            call_off_list.append(scitems.call_off)
            cmp_code.append(scitems.comp_code)

        default_cmp_code = list(set(cmp_code))

        if (CONST_CO02 in call_off_list) or (CONST_CO03 in call_off_list) or (CONST_CO04 in call_off_list):
            purch_worklist_flag = True
            completion_work_flow = get_completion_work_flow(client, prod_cat_list, default_cmp_code[0])
            if completion_work_flow:
                guid_completion.append(sc_header_guid['guid'])
                guid_completion.append(completion_work_flow[0])
                sc_completion.append(guid_completion)
        requester_first_name = requester_field_info(sc_header_guid['requester'], 'first_name')
        sc_header.append(sc_header_guid)

        for data in sc_approval:
            # get work flow manager's first name
            if data['app_id'] != CONST_AUTO and data['app_id'] != CONST_MULTIPLE:
                data['app_id'] = django_query_instance.django_filter_value_list_query(UserData, {
                    'client': client, 'username': data['app_id']
                }, 'first_name')[0]
            sc_appr.append(data)

    return sc_header, sc_appr, sc_completion, requester_first_name


# Workflow specific
def get_sc_header_app_wf(result, client):
    approver_details = []
    for sc_header_guid in result:
        sc_header_guid['first_name'] = requester_field_info(sc_header_guid['created_by'], 'first_name')
        sc_approval = django_query_instance.django_filter_only_query(ScPotentialApproval, {
            'app_id': global_variables.GLOBAL_LOGIN_USERNAME,
            'proc_lvl_sts': CONST_ACTIVE,
            'sc_header_guid': sc_header_guid['guid'],
            'client': client
        }).order_by('sc_header_guid')

        array_init = []
        for data in sc_approval:
            if sc_approval.count() != 1:
                array_init = []
            array_init.append(sc_header_guid['guid'])
            array_init.append(sc_header_guid['created_at'])
            array_init.append(sc_header_guid['description'])
            array_init.append(sc_header_guid['doc_number'])
            array_init.append(sc_header_guid['total_value'])
            array_init.append(sc_header_guid['currency'])
            array_init.append(sc_header_guid['status'])
            array_init.append(sc_header_guid['first_name'])
            array_init.append(data.app_id)

            if sc_approval.count() != 1:
                approver_details.append(array_init)
        if sc_approval.count() == 1:
            approver_details.append(array_init)
    return approver_details


# End of work flow specific


# sc completion specific
def get_header_based_on_calloff(search_fields):
    """

    :return:
    """
    document_search_instance = DocumentSearch('', '')
    header_data = []
    org_model = django_query_instance.django_get_query(OrgModel, {
        'object_id': global_variables.GLOBAL_LOGIN_USER_OBJ_ID, 'del_ind': False
    })
    org_node_type = org_model.node_type
    parent_node_guid = org_model.parent_node_guid

    while org_node_type != CONST_PGROUP:
        org_node_type, parent_node_guid, object_id = get_nodetype_parent_guid(parent_node_guid,
                                                                              global_variables.GLOBAL_CLIENT)

    pgroup_id = django_query_instance.django_filter_value_list_query(OrgPGroup, {
        'object_id': object_id, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, 'pgroup_id')

    purch_header_guid = django_query_instance.django_filter_value_list_query(PurchasingData, {
        'purch_grp__in': pgroup_id, 'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    }, 'sc_header_guid')

    call_off = [CONST_CO02, CONST_CO03, CONST_CO04]

    scitem_call_off = django_query_instance.django_filter_only_query(ScItem, {
        'header_guid__in': purch_header_guid, 'client': global_variables.GLOBAL_CLIENT, 'call_off__in': call_off
    }).values('header_guid')

    for scitem_header in scitem_call_off:
        header_data.append(scitem_header['header_guid'])

    search_fields['guid__in'] = header_data
    search_fields['status'] = CONST_SC_HEADER_INCOMPLETE

    return document_search_instance.get_header_details(search_fields)


def get_nodetype_parent_guid(parent_guid, client):
    """

    :param parent_guid:
    :param client:
    :return:
    """
    node_type = ''
    parent_node_guid = ''
    object_id = ''

    org_detail = django_query_instance.django_filter_only_query(OrgModel, {
        'node_guid': parent_guid,
        'client': client
    }).values('node_type', 'parent_node_guid', 'object_id')

    for data in org_detail:
        parent_node_guid = data['parent_node_guid']
        node_type = data['node_type']
        object_id = data['object_id']

    return node_type, parent_node_guid, object_id


# End of SC completion specific


class DocumentSearch:
    def __init__(self, requester, created_by):
        self.client = global_variables.GLOBAL_CLIENT
        self.username = global_variables.GLOBAL_LOGIN_USERNAME
        self.requester = requester
        self.created_by = created_by

    def get_header_details(self, search_criteria):
        search_criteria['client'] = self.client
        search_criteria['del_ind'] = False
        return django_query_instance.django_filter_query(ScHeader, search_criteria, ['-created_at'], None)

    def define_search_criteria(self, searched_fields, search_type):
        document_number = searched_fields['document_number']
        document_name = searched_fields['sc_name']
        timeframe = searched_fields['timeframe']
        search_criteria = {}

        if document_number is not None and document_number != '':
            if search_type == 'my_order':
                search_criteria['requester'] = self.requester

            search_criteria['doc_number'] = document_number
            return search_criteria

        if search_type == 'my_order':
            search_criteria['requester'] = self.requester
            search_criteria['created_by'] = self.created_by

        if 'status' in searched_fields:
            status = searched_fields['status']
            if status is not None and status != '':
                search_criteria['status__in'] = status

        if document_name is not None and document_name != '':
            description = document_name
            if '*' in document_name:
                get_sc_name_list = ScHeader.get_desc_by_scname(description)
                scname_match = re.search(r'[a-zA-Z0-9]+', document_name)
                if document_name[0] == '*' and document_name[-1] == '*':
                    search_criteria['description__in'] = get_sc_name_list
                    search_criteria['description__icontains'] = scname_match.group(0)
                elif document_name[0] == '*':
                    search_criteria['description__in'] = get_sc_name_list
                    search_criteria['description__iendswith'] = scname_match.group(0)
                else:
                    search_criteria['description__in'] = get_sc_name_list
                    search_criteria['description__istartswith'] = scname_match.group(0)
            else:
                scname_list = ScHeader.get_desc_by_scname(document_name)
                scname_list.append(document_name)
                search_criteria['description__in'] = scname_list

        if timeframe is not None and timeframe != '':
            if timeframe == "Today":
                minimum_search_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                maximum_search_date = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
                search_criteria['created_at__gte'] = minimum_search_date
                search_criteria['created_at__lte'] = maximum_search_date

            else:
                days_to_subtract = int(timeframe)
                from_date = date.today() - timedelta(days=days_to_subtract)
                minimum_search_date = datetime.datetime.combine(from_date, datetime.time.min)
                maximum_search_date = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
                search_criteria['created_at__gte'] = minimum_search_date
                search_criteria['created_at__lte'] = maximum_search_date

        if 'description__istartswith' in search_criteria:
            del search_criteria['description__istartswith']

        if 'created_by' in searched_fields:
            created_by = searched_fields['created_by']
            if created_by is not None and created_by != '':
                search_criteria['created_by'] = created_by

        return search_criteria
