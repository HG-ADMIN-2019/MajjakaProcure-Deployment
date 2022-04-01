from eProc_Basic.Utilities.functions.image_type_funtions import get_image_type
from eProc_Basic.Utilities.functions.log_function import update_log_info

from eProc_Org_Model.Utilities import client
from eProc_Org_Model.models import OrgModel
import datetime
from eProc_Basic.Utilities.constants.constants import CONST_ACTION_DELETE, CONST_UNSPSC_IMAGE_TYPE
from eProc_Basic.Utilities.functions.django_query_set import bulk_create_entry_db
from eProc_Basic.Utilities.functions.get_db_query import django_query_instance
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data, FieldTypeDescription
from eProc_Configuration.models import *
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models.development_data import ApproverType, AuthorizationObject, UserRoles, OrgAttributes, \
    OrgNodeTypes, AuthorizationGroup, Authorization
from eProc_Configuration.models.development_data import AccountAssignmentCategory


def save_auth_group_data_into_db(auth_group_data):
    auth_group_db_list = []

    if auth_group_data['action'] == CONST_ACTION_DELETE:
        for auth_group_detail in auth_group_data['data']:
            django_query_instance.django_update_query(AuthorizationGroup,
                                                      {'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                       'auth_obj_id': auth_group_detail['auth_obj_id']},
                                                      {'del_ind': True,
                                                       'authorization_group_changed_at': datetime.today(),
                                                       'authorization_group_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for auth_group_detail in auth_group_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AuthorizationGroup,
                                                                {'auth_grp_guid': auth_group_detail
                                                                ['auth_grp_guid']}):
                guid = guid_generator()
                auth_group_db_dictionary = {'auth_grp_guid': guid,
                                            'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                            'auth_grp_desc': auth_group_detail['auth_grp_desc'],
                                            'auth_level': auth_group_detail['auth_level'],
                                            'auth_obj_id': AuthorizationObject.objects.get(
                                                auth_obj_id=auth_group_detail['auth_obj_id']),
                                            'del_ind': False,

                                            'authorization_group_changed_at': datetime.today(),
                                            'authorization_group_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                            'authorization_group_created_at': datetime.today(),
                                            'authorization_group_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                            }
                auth_group_db_list.append(auth_group_db_dictionary)

            else:

                django_query_instance.django_update_query(AuthorizationGroup,
                                                          {'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                           'auth_obj_id': auth_group_detail['auth_obj_id']},
                                                          {
                                                              'auth_obj_grp': auth_group_detail['auth_obj_grp'],
                                                              'auth_grp_desc': auth_group_detail['auth_grp_desc'],
                                                              'auth_level': auth_group_detail['auth_level'],
                                                              'auth_obj_id': AuthorizationObject.objects.get(
                                                                  auth_obj_id=auth_group_detail['auth_obj_id']),

                                                              'authorization_group_changed_at': datetime.today(),
                                                              'authorization_group_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,

                                                              'del_ind': False})
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(AuthorizationGroup, auth_group_db_list)
        message = MSG112
    upload_response = get_configuration_data(AuthorizationGroup, {'del_ind': False},
                                             ['auth_grp_guid', 'auth_obj_grp', 'auth_grp_desc', 'auth_level',
                                              'auth_obj_id'
                                              ])

    return upload_response, message



def save_roles_data_into_db(roles_data):
    roles_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    roles_type_field = ''
    if roles_data['action'] == CONST_ACTION_DELETE:
        for roles_detail in roles_data['data']:
            django_query_instance.django_update_query(UserRoles,
                                                      {'role': roles_detail['role']},
                                                      {'del_ind': True,
                                                       'user_roles_changed_at': datetime.today(),
                                                       'user_roles_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for roles_detail in roles_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UserRoles,
                                                                {'role': roles_detail['role']}):
                roles_db_dictionary = {'role': roles_detail['role'],
                                       'role_desc': roles_detail['role_desc'],
                                       'user_roles_created_at': datetime.today(),
                                       'user_roles_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       'user_roles_changed_at': datetime.today(),
                                       'user_roles_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                       }
                roles_db_list.append(roles_db_dictionary)
            else:
                django_query_instance.django_update_query(UserRoles,
                                                          {'role': roles_detail['role']},
                                                          {'role': roles_detail['role'],
                                                           'role_desc': roles_detail['role_desc'],
                                                           'user_roles_changed_at': datetime.today(),
                                                           'user_roles_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})
        bulk_create_entry_db(UserRoles, roles_db_list)
        fieldtypedesc_instance.update_usedFlag(roles_type_field)
        message = MSG112
    upload_response = get_configuration_data(UserRoles, {'del_ind': False}, ['role', 'role_desc'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'roles'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_address_data_into_db(address_data):
    address_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if address_data['action'] == CONST_ACTION_DELETE:
        for address_detail in address_data['data']:
            django_query_instance.django_update_query(OrgAddress,
                                                      {'address_number': address_detail['address_number']},
                                                      {'del_ind': True,
                                                       'org_address_changed_at': datetime.today(),
                                                       'org_address_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for address_detail in address_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgAddress,
                                                                {'address_number': address_detail
                                                                ['address_number']}):
                guid = guid_generator()
                address_db_dictionary = {'address_guid': guid,
                                         'address_number': address_detail['address_number'],
                                         'title': address_detail['title'],
                                         'name1': address_detail['name1'],
                                         'name2': address_detail['name2'],
                                         'street': address_detail['street'],
                                         'area': address_detail['area'],
                                         'landmark': address_detail['landmark'],
                                         'city': address_detail['city'],
                                         'postal_code': address_detail['postal_code'],
                                         'region': address_detail['region'],
                                         'mobile_number': address_detail['mobile_number'],
                                         'telephone_number': address_detail['telephone_number'],
                                         'fax_number': address_detail['fax_number'],
                                         'email': address_detail['email'],
                                         'country_code': Country.objects.get(
                                             country_code=address_detail['country_code']),
                                         'language_id': Languages.objects.get(
                                             language_id=address_detail['language_id']),
                                         'time_zone': TimeZone.objects.get(time_zone=address_detail['time_zone']),

                                         'del_ind': False,
                                         'client': OrgClients.objects.get(client=client),
                                         'org_address_changed_at': datetime.today(),
                                         'org_address_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         'org_address_created_at': datetime.today(),
                                         'org_address_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         }
                address_db_list.append(address_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgAddress,
                                                          {'address_number': address_detail['address_number']},
                                                          {'address_number': address_detail['address_number'],
                                                           'title': address_detail['title'],
                                                           'name1': address_detail['name1'],
                                                           'name2': address_detail['name2'],
                                                           'street': address_detail['street'],
                                                           'area': address_detail['area'],
                                                           'landmark': address_detail['landmark'],
                                                           'city': address_detail['city'],
                                                           'postal_code': address_detail['postal_code'],
                                                           'region': address_detail['region'],
                                                           'mobile_number': address_detail['mobile_number'],
                                                           'telephone_number': address_detail['telephone_number'],
                                                           'fax_number': address_detail['fax_number'],
                                                           'email': address_detail['email'],
                                                           'country_code': Country.objects.get(
                                                               country_code=address_detail['country_code']),
                                                           'language_id': Languages.objects.get(
                                                               language_id=address_detail['language_id']),
                                                           'time_zone': TimeZone.objects.get(
                                                               time_zone=address_detail['time_zone']),
                                                           'org_address_changed_at': datetime.today(),
                                                           'org_address_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})
        bulk_create_entry_db(OrgAddress, address_db_list)
        message = MSG112
    upload_response = get_configuration_data(OrgAddress, {'del_ind': False},
                                             ['address_guid', 'address_number', 'title', 'name1', 'name2',
                                              'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                              'mobile_number', 'telephone_number', 'fax_number', 'email',
                                              'country_code', 'language_id', 'time_zone'
                                              ])

    return upload_response, message


def save_payterm_data_into_db(payterm_data):
    payterm_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if payterm_data['action'] == CONST_ACTION_DELETE:
        for payterm_detail in payterm_data['data']:
            django_query_instance.django_update_query(Payterms,
                                                      {'payment_term_guid': payterm_detail['payment_term_guid']},
                                                      {'del_ind': True,
                                                       'payterms_changed_at': datetime.today(),
                                                       'payterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for payterm_detail in payterm_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Payterms,
                                                                {'payment_term_guid': payterm_detail
                                                                ['payment_term_guid']}):
                guid = guid_generator()
                payterm_db_dictionary = {'payment_term_guid': guid,
                                         'payment_term_key': payterm_detail['payment_term_key'],
                                         'del_ind': False,
                                         'client': client,
                                         'payterms_changed_at': datetime.today(),
                                         'payterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         'payterms_created_at': datetime.today(),
                                         'payterms_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         }
                payterm_db_list.append(payterm_db_dictionary)

            else:

                django_query_instance.django_update_query(Payterms,
                                                          {'payment_term_guid': payterm_detail['payment_term_guid']},
                                                          {'payment_term_guid': payterm_detail['payment_term_guid'],
                                                           'payment_term_key': payterm_detail['payment_term_key'],
                                                           'payterms_changed_at': datetime.today(),
                                                           'payterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(Payterms, payterm_db_list)
        message = MSG112
    upload_response = get_configuration_data(Payterms, {'del_ind': False},
                                             ['payment_term_guid', 'payment_term_key',
                                              ])

    return upload_response, message


def save_spend_limit_value_data_into_db(spend_limit_value_data):
    """

        """
    spend_limit_value_db_list = []
    client = global_variables.GLOBAL_CLIENT

    if spend_limit_value_data['action'] == CONST_ACTION_DELETE:
        for spend_limit_value_detail in spend_limit_value_data['data']:
            django_query_instance.django_update_query(SpendLimitValue,
                                                      {'spend_code_id': spend_limit_value_detail[
                                                          'spend_code_id'],
                                                       'company_id': spend_limit_value_detail[
                                                           'company_id'],
                                                       'currency_id': spend_limit_value_detail[
                                                           'currency_id']},
                                                      {'del_ind': True,
                                                       'spend_limit_value_changed_at': datetime.today(),
                                                       'spend_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for spend_limit_value_detail in spend_limit_value_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(SpendLimitValue,
                                                                {'spend_code_id': spend_limit_value_detail[
                                                                    'spend_code_id'],
                                                                 'spend_lim_value_guid': spend_limit_value_detail[
                                                                     'spend_lim_value_guid'],
                                                                 'company_id': spend_limit_value_detail[
                                                                     'company_id'],
                                                                 'currency_id': spend_limit_value_detail[
                                                                     'currency_id']}):
                guid = guid_generator()
                spend_limit_value_db_dictionary = {'spend_lim_value_guid': guid,
                                                   'spend_code_id': spend_limit_value_detail['spend_code_id'],
                                                   'upper_limit_value': spend_limit_value_detail['upper_limit_value'],
                                                   'company_id': spend_limit_value_detail['company_id'],
                                                   'currency_id': Currency.objects.get(
                                                       currency_id=spend_limit_value_detail['currency_id']),
                                                   'del_ind': False,
                                                   'client': client,
                                                   'spend_limit_value_created_at': datetime.today(),
                                                   'spend_limit_value_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'spend_limit_value_changed_at': datetime.today(),
                                                   'spend_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                                   }
                spend_limit_value_db_list.append(spend_limit_value_db_dictionary)
            else:
                django_query_instance.django_update_query(SpendLimitValue,
                                                          {'spend_code_id': spend_limit_value_detail[
                                                              'spend_code_id'],
                                                           'company_id': spend_limit_value_detail[
                                                               'company_id'],
                                                           'currency_id': spend_limit_value_detail[
                                                               'currency_id']},
                                                          {'spend_lim_value_guid': spend_limit_value_detail[
                                                              'spend_lim_value_guid'],
                                                           'spend_code_id': spend_limit_value_detail['spend_code_id'],
                                                           'upper_limit_value': spend_limit_value_detail[
                                                               'upper_limit_value'],
                                                           'company_id': spend_limit_value_detail['company_id'],
                                                           'currency_id': spend_limit_value_detail['currency_id'],
                                                           'client': client,
                                                           'spend_limit_value_changed_at': datetime.today(),
                                                           'spend_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False
                                                           })
        bulk_create_entry_db(SpendLimitValue, spend_limit_value_db_list)
        message = MSG112
    upload_response = get_configuration_data(SpendLimitValue, {'del_ind': False},
                                             ['spend_lim_value_guid', 'spend_code_id', 'upper_limit_value',
                                              'company_id', 'currency_id'])
    return upload_response, message


def save_approval_data_into_db(approval_data):
    """

    """
    approval_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    appr_type_field = ''
    if approval_data['action'] == CONST_ACTION_DELETE:
        for approval_detail in approval_data['data']:
            appr_type_field = approval_detail['app_types']
            django_query_instance.django_update_query(ApproverType,
                                                      {'app_types': approval_detail['app_types']},
                                                      {'del_ind': True,
                                                       'approver_type_changed_at': datetime.today(),
                                                       'approver_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        fieldtypedesc_instance.reset_usedFlag(appr_type_field)
        message = MSG113
    else:
        for approval_detail in approval_data['data']:
            appr_type_field = approval_detail['app_types']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverType,
                                                                {'app_types': approval_detail[
                                                                    'app_types']}):
                approval_db_dictionary = {'app_types': approval_detail['app_types'],
                                          'appr_type_desc': approval_detail['appr_type_desc'],
                                          'del_ind': False,
                                          'approver_type_created_at': datetime.today(),
                                          'approver_type_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                          'approver_type_changed_at': datetime.today(),
                                          'approver_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                          }
                approval_db_list.append(approval_db_dictionary)
            else:
                django_query_instance.django_update_query(ApproverType,
                                                          {'app_types': approval_detail[
                                                              'app_types']},
                                                          {'app_types': approval_detail[
                                                              'app_types'],
                                                           'appr_type_desc': approval_detail['appr_type_desc'],
                                                           'approver_type_changed_at': datetime.today(),
                                                           'approver_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False
                                                           })
        bulk_create_entry_db(ApproverType, approval_db_list)
        fieldtypedesc_instance.update_usedFlag(appr_type_field)
        message = MSG112
    upload_response = get_configuration_data(ApproverType, {'del_ind': False},
                                             ['app_types', 'appr_type_desc'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'approval_type'},
                                                                             ['field_type_id', 'field_type_desc'])
    return upload_response, message, upload_fieldtypedesc


def save_app_limit_value_data_into_db(applimval_data):
    applimval_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if applimval_data['action'] == CONST_ACTION_DELETE:
        for applimval_detail in applimval_data['data']:
            django_query_instance.django_update_query(ApproverLimitValue,
                                                      {'app_code_id': applimval_detail['app_code_id'],
                                                       'app_lim_dec_guid': applimval_detail['app_lim_dec_guid'],
                                                       'company_id': applimval_detail['company_id'],
                                                       'app_types': applimval_detail['app_types'],
                                                       'currency_id': applimval_detail['currency_id']},
                                                      {'del_ind': True,
                                                       'approver_limit_value_changed_at': datetime.today(),
                                                       'approver_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for applimval_detail in applimval_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverLimitValue,
                                                                {'app_code_id': applimval_detail['app_code_id'],
                                                                 'app_lim_dec_guid': applimval_detail[
                                                                     'app_lim_dec_guid'],
                                                                 'company_id': applimval_detail['company_id'],
                                                                 'app_types': applimval_detail['app_types'],
                                                                 'currency_id': applimval_detail['currency_id']}):
                guid = guid_generator()
                applimval_db_dictionary = {'app_lim_dec_guid': guid,
                                           'app_types': ApproverType.objects.get(
                                               app_types=applimval_detail['app_types']),
                                           'app_code_id': applimval_detail['app_code_id'],
                                           'upper_limit_value': applimval_detail['upper_limit_value'],
                                           'company_id': applimval_detail['company_id'],
                                           'currency_id': Currency.objects.get(
                                               currency_id=applimval_detail['currency_id']),
                                           'del_ind': False,
                                           'client': client,
                                           'approver_limit_value_changed_at': datetime.today(),
                                           'approver_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'approver_limit_value_created_at': datetime.today(),
                                           'approver_limit_value_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           }

                applimval_db_list.append(applimval_db_dictionary)

            else:

                django_query_instance.django_update_query(ApproverLimitValue,
                                                          {'app_code_id': applimval_detail['app_code_id'],
                                                           'company_id': applimval_detail['company_id'],
                                                           'app_types': applimval_detail['app_types'],
                                                           'currency_id': applimval_detail['currency_id']},
                                                          {'app_lim_dec_guid': applimval_detail['app_lim_dec_guid'],
                                                           'app_types': applimval_detail['app_types'],
                                                           'app_code_id': applimval_detail['app_code_id'],
                                                           'upper_limit_value': applimval_detail['upper_limit_value'],
                                                           'company_id': applimval_detail['company_id'],
                                                           'currency_id': applimval_detail['currency_id'],
                                                           'client': client,
                                                           'del_ind': False,
                                                           'approver_limit_value_changed_at': datetime.today(),
                                                           'approver_limit_value_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           })
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(ApproverLimitValue, applimval_db_list)
        message = MSG112
    upload_response = get_configuration_data(ApproverLimitValue, {'del_ind': False},
                                             ['app_lim_dec_guid', 'app_types',
                                              'app_code_id', 'upper_limit_value',
                                              'company_id', 'currency_id'])

    return upload_response, message


def save_app_limit_data_into_db(applim_data):
    applim_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if applim_data['action'] == CONST_ACTION_DELETE:
        for applim_detail in applim_data['data']:
            django_query_instance.django_update_query(ApproverLimit,
                                                      {'approver_username': applim_detail['approver_username'],
                                                       'app_guid': applim_detail['app_guid'],
                                                       'company_id': applim_detail['company_id'],
                                                       'app_code_id': applim_detail['app_code_id'],
                                                       },
                                                      {'del_ind': True,
                                                       'approver_limit_changed_at': datetime.today(),
                                                       'approver_limit_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for applim_detail in applim_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(ApproverLimit,
                                                                {'approver_username': applim_detail[
                                                                    'approver_username'],
                                                                 'app_code_id': applim_detail['app_code_id'],
                                                                 'app_guid': applim_detail['app_guid'],
                                                                 'company_id': applim_detail['company_id']}):
                guid = guid_generator()
                applim_db_dictionary = {'app_guid': guid,
                                        'approver_username': applim_detail['approver_username'],
                                        'app_code_id': applim_detail['app_code_id'],
                                        'company_id': applim_detail['company_id'],
                                        'del_ind': False,
                                        'client': client,
                                        'approver_limit_changed_at': datetime.today(),
                                        'approver_limit_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                        'approver_limit_created_at': datetime.today(),
                                        'approver_limit_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                        }
                applim_db_list.append(applim_db_dictionary)

            else:

                django_query_instance.django_update_query(ApproverLimit,
                                                          {'approver_username': applim_detail['approver_username'],
                                                           'app_code_id': applim_detail['app_code_id'],
                                                           'company_id': applim_detail['company_id']},
                                                          {'app_guid': applim_detail['app_guid'],
                                                           'approver_username': applim_detail['approver_username'],
                                                           'app_code_id': applim_detail['app_code_id'],
                                                           'company_id': applim_detail['company_id'],
                                                           'approver_limit_changed_at': datetime.today(),
                                                           'approver_limit_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(ApproverLimit, applim_db_list)
        message = MSG112
    upload_response = get_configuration_data(ApproverLimit, {'del_ind': False},
                                             ['app_guid', 'approver_username',
                                              'app_code_id',
                                              'company_id', ])

    return upload_response, message


def save_aad_data_into_db(aad_data):
    aad_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if aad_data['action'] == CONST_ACTION_DELETE:
        for aad_detail in aad_data['data']:
            django_query_instance.django_update_query(AccountingDataDesc,
                                                      {'account_assign_value': aad_detail['account_assign_value'],
                                                       'account_assign_cat': aad_detail['account_assign_cat'],
                                                       'company_id': aad_detail['company_id'],
                                                       'language_id': aad_detail['language_id']},
                                                      {'del_ind': True,
                                                       'accounting_data_desc_changed_at': datetime.today(),
                                                       'accounting_data_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for aad_detail in aad_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountingDataDesc,
                                                                {'account_assign_value': aad_detail[
                                                                    'account_assign_value'],
                                                                 'account_assign_cat': aad_detail['account_assign_cat'],
                                                                 'company_id': aad_detail['company_id'],
                                                                 'language_id': aad_detail['language_id']}):
                guid = guid_generator()
                aad_db_dictionary = {'acc_desc_guid': guid,
                                     'account_assign_value': aad_detail['account_assign_value'],
                                     'description': aad_detail['description'],
                                     'account_assign_cat': AccountAssignmentCategory.objects.get(
                                         account_assign_cat=aad_detail['account_assign_cat']),
                                     'company_id': aad_detail['company_id'],
                                     'language_id': Languages.objects.get(
                                         language_id=aad_detail['language_id']),
                                     'del_ind': False,
                                     'client': client,
                                     'accounting_data_desc_changed_at': datetime.today(),
                                     'accounting_data_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                     'accounting_data_desc_created_at': datetime.today(),
                                     'accounting_data_desc_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                     }
                aad_db_list.append(aad_db_dictionary)

            else:

                django_query_instance.django_update_query(AccountingDataDesc,
                                                          {'account_assign_value': aad_detail['account_assign_value'],
                                                           'account_assign_cat': aad_detail['account_assign_cat'],
                                                           'company_id': aad_detail['company_id'],
                                                           'language_id': aad_detail['language_id']},
                                                          {'account_assign_value': aad_detail['account_assign_value'],
                                                           'description': aad_detail['description'],
                                                           'account_assign_cat': aad_detail['account_assign_cat'],
                                                           'company_id': aad_detail['company_id'],
                                                           'language_id': aad_detail['language_id'],
                                                           'accounting_data_desc_changed_at': datetime.today(),
                                                           'accounting_data_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': aad_detail['del_ind']})
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(AccountingDataDesc, aad_db_list)
        message = MSG112
    upload_response = get_configuration_data(AccountingDataDesc, {'del_ind': False},
                                             ['acc_desc_guid', 'account_assign_value',
                                              'description',
                                              'account_assign_cat', 'company_id', 'language_id'
                                              ])

    return upload_response, message


def save_workflow_acc_data_into_db(wfacc_data):
    """

    """
    wfacc_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if wfacc_data['action'] == CONST_ACTION_DELETE:
        for wfacc_detail in wfacc_data['data']:
            django_query_instance.django_update_query(WorkflowACC,
                                                      {'workflow_acc_guid': wfacc_detail['workflow_acc_guid']},
                                                      {'del_ind': True,
                                                       'workflow_acc_changed_at': datetime.today(),
                                                       'workflow_acc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for wfacc_detail in wfacc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(WorkflowACC,
                                                                {'workflow_acc_guid': wfacc_detail[
                                                                    'workflow_acc_guid']}):
                guid = guid_generator()
                wfacc_db_dictionary = {'workflow_acc_guid': guid,
                                       'acc_value': wfacc_detail['acc_value'],
                                       'company_id': wfacc_detail['company_id'],
                                       'app_username': wfacc_detail['app_username'],
                                       'sup_company_id': wfacc_detail['sup_company_id'],
                                       'sup_acc_value': wfacc_detail['sup_acc_value'],
                                       'account_assign_cat': AccountAssignmentCategory.objects.get
                                       (account_assign_cat=wfacc_detail['account_assign_cat']),
                                       'sup_account_assign_cat': AccountAssignmentCategory.objects.get
                                       (account_assign_cat=wfacc_detail['sup_account_assign_cat']),
                                       'currency_id': Currency.objects.get(currency_id=wfacc_detail['sup_currency_id']),
                                       'del_ind': False,
                                       'workflow_acc_created_at': datetime.today(),
                                       'workflow_acc_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       'workflow_acc_changed_at': datetime.today(),
                                       'workflow_acc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       'client': client,
                                       }
                wfacc_db_list.append(wfacc_db_dictionary)
            else:
                django_query_instance.django_update_query(WorkflowACC,
                                                          {'workflow_acc_guid': wfacc_detail[
                                                              'workflow_acc_guid']},
                                                          {'workflow_acc_guid': wfacc_detail[
                                                              'workflow_acc_guid'],
                                                           'acc_value': wfacc_detail['acc_value'],
                                                           'company_id': wfacc_detail['company_id'],
                                                           'app_username': wfacc_detail['app_username'],
                                                           'sup_company_id': wfacc_detail['sup_company_id'],
                                                           'sup_acc_value': wfacc_detail['sup_acc_value'],
                                                           'account_assign_cat': wfacc_detail['account_assign_cat'],
                                                           'sup_account_assign_cat': wfacc_detail[
                                                               'sup_account_assign_cat'],
                                                           'currency_id': wfacc_detail[
                                                               'sup_currency_id'],
                                                           'workflow_acc_changed_at': datetime.today(),
                                                           'workflow_acc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False,
                                                           'client': OrgClients.objects.get(client=client),
                                                           })
        bulk_create_entry_db(WorkflowACC, wfacc_db_list)
        message = MSG112
    upload_response = get_configuration_data(WorkflowACC, {'del_ind': False},
                                             ['workflow_acc_guid', 'acc_value', 'company_id', 'app_username',
                                              'sup_company_id',
                                              'sup_acc_value', 'account_assign_cat', 'sup_account_assign_cat',
                                              'currency_id'])
    return upload_response, message


def save_payment_desc_data_into_db(payment_desc_data):
    """

    """
    payment_desc_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if payment_desc_data['action'] == CONST_ACTION_DELETE:
        for payment_desc_detail in payment_desc_data['data']:
            django_query_instance.django_update_query(Payterms_desc,
                                                      {'payment_term_key': payment_desc_detail['payment_term_key'],
                                                       'language_id': payment_desc_detail['language_id']},
                                                      {'del_ind': True,
                                                       'payterms_desc_changed_at': datetime.today(),
                                                       'payterms_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for payment_desc_detail in payment_desc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Payterms_desc,
                                                                {'payment_term_key': payment_desc_detail[
                                                                    'payment_term_key'],
                                                                 'language_id': payment_desc_detail['language_id'],
                                                                 'del_ind': False}):
                guid = guid_generator()
                payment_desc_db_dictionary = {'payment_term_guid': guid,
                                              'payment_term_key': payment_desc_detail['payment_term_key'],
                                              'day_limit': payment_desc_detail['day_limit'],
                                              'description': payment_desc_detail['description'],
                                              'language_id': Languages.objects.get(
                                                  language_id=payment_desc_detail['language_id']),
                                              'del_ind': False,
                                              'client': client,
                                              'payterms_desc_created_at': datetime.today(),
                                              'payterms_desc_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                              'payterms_desc_changed_at': datetime.today(),
                                              'payterms_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                              }
                payment_desc_db_list.append(payment_desc_db_dictionary)
            else:
                django_query_instance.django_update_query(Payterms_desc,
                                                          {'payment_term_key': payment_desc_detail['payment_term_key'],
                                                           'language_id': payment_desc_detail['language_id']},
                                                          {'payment_term_guid': payment_desc_detail[
                                                              'payment_term_guid'],
                                                           'payment_term_key': payment_desc_detail['payment_term_key'],
                                                           'day_limit': payment_desc_detail['day_limit'],
                                                           'description': payment_desc_detail['description'],
                                                           'language_id': payment_desc_detail['language_id'],
                                                           'payterms_desc_changed_at': datetime.today(),
                                                           'payterms_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False,
                                                           'client': client
                                                           })
        bulk_create_entry_db(Payterms_desc, payment_desc_db_list)
        message = MSG112
    upload_response = get_configuration_data(Payterms_desc, {'del_ind': False},
                                             ['payment_term_guid', 'payment_term_key', 'day_limit',
                                              'description', 'language_id'])
    return upload_response, message


def save_incoterms_data_into_db(incoterms_data):
    """

    """
    incoterms_db_list = []
    if incoterms_data['action'] == CONST_ACTION_DELETE:
        for incoterms_detail in incoterms_data['data']:
            django_query_instance.django_update_query(Incoterms,
                                                      {'incoterm_key': incoterms_detail['incoterm_key']},
                                                      {'del_ind': True,
                                                       'incoterms_changed_at': datetime.today(),
                                                       'incoterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for incoterms_detail in incoterms_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Incoterms,
                                                                {'incoterm_key': incoterms_detail[
                                                                    'incoterm_key']}):
                incoterms_db_dictionary = {'incoterm_key': incoterms_detail['incoterm_key'],
                                           'description': incoterms_detail['description'],
                                           'del_ind': False,
                                           'incoterms_created_at': datetime.today(),
                                           'incoterms_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'incoterms_changed_at': datetime.today(),
                                           'incoterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                           }
                incoterms_db_list.append(incoterms_db_dictionary)
            else:
                django_query_instance.django_update_query(Incoterms,
                                                          {'incoterm_key': incoterms_detail[
                                                              'incoterm_key']},
                                                          {'incoterm_key': incoterms_detail[
                                                              'incoterm_key'],
                                                           'description': incoterms_detail['description'],
                                                           'incoterms_changed_at': datetime.today(),
                                                           'incoterms_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False
                                                           })
        bulk_create_entry_db(Incoterms, incoterms_db_list)
        message = MSG112
    upload_response = get_configuration_data(Incoterms, {'del_ind': False},
                                             ['incoterm_key', 'description'])
    return upload_response, message


def save_aav_data_into_db(aav_data):
    """

    """
    aav_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if aav_data['action'] == CONST_ACTION_DELETE:
        for aav_detail in aav_data['data']:
            django_query_instance.django_update_query(AccountingData,
                                                      {'account_assign_value': aav_detail['account_assign_value'],
                                                       'account_assign_cat': aav_detail['account_assign_cat'],
                                                       'company_id': aav_detail['company_id']},
                                                      {'del_ind': True,
                                                       'accounting_data_changed_at': datetime.today(),
                                                       'accounting_data_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for aav_detail in aav_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountingData,
                                                                {'account_assign_value': aav_detail['account_assign_value'],
                                                                 'account_assign_cat': aav_detail['account_assign_cat'],
                                                                 'company_id': aav_detail['company_id']}):
                guid = guid_generator()
                aav_db_dictionary = {'account_assign_guid': guid,
                                     'account_assign_value': aav_detail['account_assign_value'],
                                     'account_assign_cat': AccountAssignmentCategory.objects.get(
                                         account_assign_cat=aav_detail['account_assign_cat']),
                                     'valid_from': aav_detail['valid_from'],
                                     'valid_to': aav_detail['valid_to'],
                                     'company_id': aav_detail['company_id'],
                                     'del_ind': False,
                                     'client': client,
                                     'accounting_data_changed_at': datetime.today(),
                                     'accounting_data_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                     'accounting_data_created_at': datetime.today(),
                                     'accounting_data_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                     }

                aav_db_list.append(aav_db_dictionary)

            else:

                django_query_instance.django_update_query(AccountingData,
                                                          {'account_assign_value': aav_detail['account_assign_value'],
                                                           'account_assign_cat': aav_detail['account_assign_cat'],
                                                           'company_id': aav_detail['company_id']},
                                                          {'account_assign_value': aav_detail['account_assign_value'],
                                                           'account_assign_cat': aav_detail['account_assign_cat'],
                                                           'valid_from': aav_detail['valid_from'],
                                                           'valid_to': aav_detail['valid_to'],
                                                           'company_id': aav_detail['company_id'],
                                                           'accounting_data_changed_at': datetime.today(),
                                                           'accounting_data_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})

        bulk_create_entry_db(AccountingData, aav_db_list)
        message = MSG112
    upload_response = get_configuration_data(AccountingData, {'del_ind': False},
                                             ['account_assign_guid', 'account_assign_value',
                                              'account_assign_cat', 'valid_from',
                                              'valid_to', 'company_id'])

    return upload_response, message


def save_purgrp_data_into_db(pggrp_data):
    pggrp_data_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if pggrp_data['action'] == CONST_ACTION_DELETE:
        for pggrp_detail in pggrp_data['data']:
            django_query_instance.django_update_query(OrgPGroup,
                                                      {'pgroup_id': pggrp_detail['pgroup_id'],
                                                       'porg_id': pggrp_detail['porg_id']},
                                                      {'del_ind': True,
                                                       'org_pgroup_changed_at': datetime.today(),
                                                       'org_pgroup_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for pggrp_detail in pggrp_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgPGroup,
                                                                {'pgroup_id': pggrp_detail['pgroup_id']
                                                                 }):
                guid = guid_generator()
                pggrp_db_dictionary = {'pgroup_guid': guid,
                                       'pgroup_id': pggrp_detail['pgroup_id'],
                                       'description': pggrp_detail['description'],
                                       'porg_id': pggrp_detail['porg_id'],
                                       'object_id': OrgModel.objects.get(
                                           object_id=pggrp_detail['object_id']),
                                       'del_ind': False,
                                       'client': client,
                                       'org_pgroup_changed_at': datetime.today(),
                                       'org_pgroup_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       'org_pgroup_created_at': datetime.today(),
                                       'org_pgroup_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       }

                pggrp_data_db_list.append(pggrp_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgPGroup,
                                                          {'pgroup_id': pggrp_detail['pgroup_id']},
                                                          {'pgroup_id': pggrp_detail['pgroup_id'],
                                                           'description': pggrp_detail['description'],
                                                           'porg_id': pggrp_detail['porg_id'],
                                                           'object_id': OrgModel.objects.get(
                                                               object_id=pggrp_detail['object_id']),
                                                           'org_pgroup_changed_at': datetime.today(),
                                                           'org_pgroup_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': pggrp_detail['del_ind']})

        bulk_create_entry_db(OrgPGroup, pggrp_data_db_list)
        message = MSG112
    upload_response = get_configuration_data(OrgPGroup, {'del_ind': False},
                                             ['pgroup_guid', 'pgroup_id',
                                              'description', 'porg_id','object_id' ])

    return upload_response, message


def save_purorg_data_into_db(pgorg_data):
    pgorg_data_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if pgorg_data['action'] == CONST_ACTION_DELETE:
        for pgorg_detail in pgorg_data['data']:
            django_query_instance.django_update_query(OrgPorg,
                                                      {'porg_id': pgorg_detail['porg_id'],
                                                       'company_id': pgorg_detail['company_id']},
                                                      {'del_ind': True,
                                                       'org_porg_changed_at': datetime.today(),
                                                       'org_porg_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for pgorg_detail in pgorg_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgPorg,
                                                                {'porg_id': pgorg_detail['porg_id'],
                                                                 'company_id': pgorg_detail['company_id']}):
                guid = guid_generator()
                pgorg_db_dictionary = {'porg_guid': guid,
                                       'porg_id': pgorg_detail['porg_id'],
                                       'description': pgorg_detail['description'],
                                       'company_id': pgorg_detail['company_id'],
                                       'object_id': OrgModel.objects.get(
                                           object_id=pgorg_detail['object_id']),
                                       'del_ind': False,
                                       'client': client,
                                       'org_porg_changed_at': datetime.today(),
                                       'org_porg_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       'org_porg_created_at': datetime.today(),
                                       'org_porg_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                       }

                pgorg_data_db_list.append(pgorg_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgPorg,
                                                          {'porg_id': pgorg_detail['porg_id'],
                                                           'company_id': pgorg_detail['company_id']},
                                                          {'porg_id': pgorg_detail['porg_id'],
                                                           'description': pgorg_detail['description'],
                                                           'company_id': pgorg_detail['company_id'],
                                                           'object_id': OrgModel.objects.get(
                                                               object_id=pgorg_detail['object_id']),
                                                           'org_porg_changed_at': datetime.today(),
                                                           'org_porg_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': pgorg_detail['del_ind']})

        bulk_create_entry_db(OrgPorg, pgorg_data_db_list)
        message = MSG112
    upload_response = get_configuration_data(OrgPorg, {'del_ind': False},
                                             ['porg_guid', 'porg_id',
                                              'description','company_id', 'object_id'])

    return upload_response, message


def save_orgnode_types_data_into_db(orgnode_data):
    orgnode_data_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    nod_type_field = ''
    client = global_variables.GLOBAL_CLIENT
    if orgnode_data['action'] == CONST_ACTION_DELETE:
        for orgnode_detail in orgnode_data['data']:
            nod_type_field = orgnode_detail['node_type']
            django_query_instance.django_update_query(OrgNodeTypes,
                                                      {'node_type': orgnode_detail['node_type'],
                                                       'client': global_variables.GLOBAL_CLIENT},
                                                      {'del_ind': True,
                                                       'org_node_types_changed_at': datetime.today(),
                                                       'org_node_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
            fieldtypedesc_instance.reset_usedFlag(nod_type_field)
            message = MSG113
    else:
        for orgnode_detail in orgnode_data['data']:
            # if entry is not exists in db
            nod_type_field = orgnode_detail['node_type']
            if not django_query_instance.django_existence_check(OrgNodeTypes,
                                                                {'node_type': orgnode_detail['node_type'],
                                                                 'client': global_variables.GLOBAL_CLIENT}):
                guid = guid_generator()
                orgnode_db_dictionary = {'node_type_guid': guid,
                                         'node_type': orgnode_detail['node_type'],
                                         'description': orgnode_detail['description'],
                                         'del_ind': False,
                                         'client': client,
                                         'org_node_types_changed_at': datetime.today(),
                                         'org_node_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         'org_node_types_created_at': datetime.today(),
                                         'org_node_types_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         }

                orgnode_data_db_list.append(orgnode_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgNodeTypes,
                                                          {'node_type': orgnode_detail['node_type'],
                                                           'client': global_variables.GLOBAL_CLIENT},
                                                          {'node_type_guid': orgnode_detail['node_type_guid'],
                                                           'node_type': orgnode_detail['node_type'],
                                                           'description': orgnode_detail['description'],
                                                           'org_node_types_changed_at': datetime.today(),
                                                           'org_node_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})

        bulk_create_entry_db(OrgNodeTypes, orgnode_data_db_list)
        fieldtypedesc_instance.update_usedFlag(nod_type_field)
        message = MSG112

    upload_response = get_configuration_data(OrgNodeTypes, {'del_ind': False, 'client': global_variables.GLOBAL_CLIENT},
                                             ['node_type_guid', 'node_type',
                                              'description'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'node_type'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_orgattributes_data_into_db(attr_data):
    attr_data_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    att_type_field = ''


    if attr_data['action'] == CONST_ACTION_DELETE:
        for attr_detail in attr_data['data']:
            att_type_field = attr_detail['attribute_id']
            django_query_instance.django_update_query(OrgAttributes,
                                                      {'attribute_id': attr_detail['attribute_id']},
                                                      {'del_ind': True,
                                                       'org_attributes_changed_at': datetime.today(),
                                                       'org_attributes_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )

            fieldtypedesc_instance.reset_usedFlag(att_type_field)
        message = MSG113
    else:
        for attr_detail in attr_data['data']:
            # if entry is not exists in db
            att_type_field = attr_detail['attribute_id']
            if not django_query_instance.django_existence_check(OrgAttributes,
                                                                {'attribute_id': attr_detail['attribute_id']}):

                attr_db_dictionary = {'attribute_id': attr_detail['attribute_id'],
                                      'attribute_name': attr_detail['attribute_name'],
                                      'range_indicator': attr_detail['range_indicator'],
                                      'multiple_value': attr_detail['multiple_value'],
                                      'allow_defaults': attr_detail['allow_defaults'],
                                      'inherit_values': attr_detail['inherit_values'],
                                      'maximum_length': attr_detail['maximum_length'],
                                      'del_ind': False,
                                      'org_attributes_changed_at': datetime.today(),
                                      'org_attributes_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                      'org_attributes_created_at': datetime.today(),
                                      'org_attributes_created_by': global_variables.GLOBAL_LOGIN_USERNAME}

                attr_data_db_list.append(attr_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgAttributes,
                                                          {'attribute_id': attr_detail['attribute_id']},
                                                          {'attribute_id': attr_detail['attribute_id'],
                                                           'attribute_name': attr_detail['attribute_name'],
                                                           'range_indicator': attr_detail['range_indicator'],
                                                           'multiple_value': attr_detail['multiple_value'],
                                                           'allow_defaults': attr_detail['allow_defaults'],
                                                           'inherit_values': attr_detail['inherit_values'],
                                                           'maximum_length': attr_detail['maximum_length'],
                                                           'org_attributes_changed_at': datetime.today(),
                                                           'org_attributes_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})

        bulk_create_entry_db(OrgAttributes, attr_data_db_list)
        fieldtypedesc_instance.update_usedFlag(att_type_field)
        message = MSG112
    upload_response = get_configuration_data(OrgAttributes, {'del_ind': False},
                                             ['attribute_id', 'attribute_name',
                                              'range_indicator', 'multiple_value',
                                              'allow_defaults', 'inherit_values',
                                              'maximum_length'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'attribute_id'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_authorobject_data_into_db(authobj_data):
    authobj_data_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    # fieldtypedesc_instance1 = FieldTypeDescription()
    auth_obj_field = ''
    auth_type_field = ''
    if authobj_data['action'] == CONST_ACTION_DELETE:
        for authobj_detail in authobj_data['data']:
            auth_obj_field = authobj_data['auth_obj_id']

            auth_type_field = authobj_data['auth_level']

            django_query_instance.django_update_query(AuthorizationObject,
                                                      {'auth_obj_id': authobj_detail['auth_obj_id'],
                                                       'auth_level': authobj_detail['auth_level']},
                                                      {'del_ind': True,
                                                       'authorization_object_changed_at': datetime.today(),
                                                       'authorization_object_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
            fieldtypedesc_instance.reset_usedFlag(auth_obj_field)
            fieldtypedesc_instance.reset_usedFlag(auth_type_field)
        message = MSG113
    else:
        for authobj_detail in authobj_data['data']:
            # if entry is not exists in db
            auth_obj_field = authobj_detail['auth_obj_id']
            auth_type_field = authobj_detail['auth_level']
            if not django_query_instance.django_existence_check(AuthorizationObject,
                                                                {'auth_obj_id': authobj_detail['auth_obj_id']}):

                authobj_db_dictionary = {'auth_obj_id': authobj_detail['auth_obj_id'],
                                         'auth_level_ID': authobj_detail['auth_level_ID'],
                                         'auth_level': authobj_detail['auth_level'],
                                         'del_ind': False,
                                         'authorization_object_changed_at': datetime.today(),
                                         'authorization_object_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         'authorization_object_created_at': datetime.today(),
                                         'authorization_object_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         }

                authobj_data_db_list.append(authobj_db_dictionary)

            else:

                django_query_instance.django_update_query(AuthorizationObject,
                                                          {'auth_obj_id': authobj_detail['auth_obj_id']},
                                                          {'auth_obj_id': authobj_detail['auth_obj_id'],
                                                           'auth_level_ID': authobj_detail['auth_level_ID'],
                                                           'auth_level': authobj_detail['auth_level'],
                                                           'authorization_object_changed_at': datetime.today(),
                                                           'authorization_object_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})

        bulk_create_entry_db(AuthorizationObject, authobj_data_db_list)
        fieldtypedesc_instance.update_usedFlag(auth_obj_field)
        fieldtypedesc_instance.update_usedFlag(auth_type_field)
        message = MSG112
    upload_response = get_configuration_data(AuthorizationObject, {'del_ind': False},
                                             ['auth_obj_id','auth_level_ID',
                                              'auth_level'])

    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'auth_obj_id'},
                                                                             ['field_type_id', 'field_type_desc'])

    upload_fieldtypedesc1 = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'auth_level'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc,upload_fieldtypedesc1


def save_master_data_into_db(master_data, Table, client):
    """
    save master data to db
    :param master_data:
    :return:
    """

    # try:

    if Table == 'upload_apptypes':

        Success_message = MSG037

        apptypes_not_exist: object = ApproverType.objects.filter(del_ind=False).exclude(
            app_types__in=[apptypes['app_types'] for apptypes in master_data])

        for set_del_int in apptypes_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()
        for save_apptypes in master_data:
            if not (ApproverType.objects.filter(app_types=save_apptypes['app_types'],
                                                appr_type_desc=save_apptypes['appr_type_desc'],
                                                del_ind=False).exists()):
                obj, created = ApproverType.objects.update_or_create(
                    app_types=save_apptypes['app_types'],
                    defaults={'app_types': save_apptypes['app_types'],
                              'appr_type_desc': save_apptypes['appr_type_desc'],
                              'del_ind': False},
                )

        return True, Success_message

    if Table == 'upload_roles':

        for save_roles in master_data:
            if save_roles['del_ind']:
                UserRoles.objects.filter(role=save_roles['role']).update(del_ind=True)

            else:
                created_at_val = django_query_instance.django_filter_value_list_query(UserRoles, {
                    'role': save_roles['role'], 'del_ind': False},
                                                                                      'user_roles_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(UserRoles, {
                    'role': save_roles['role'], 'del_ind': False},
                                                                                      'user_roles_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                if not (UserRoles.objects.filter(role=save_roles['role'], role_desc=save_roles['role_desc'],
                                                 del_ind=False).exists()):
                    obj, created = UserRoles.objects.update_or_create(
                        role=save_roles['role'],
                        defaults={'role': save_roles['role'],
                                  'role_desc': save_roles['role_desc'],
                                  'user_roles_created_at': created_time_val,
                                  'user_roles_created_by': created_by_val,
                                  'user_roles_changed_at': changed_at_val,
                                  'user_roles_changed_by': changed_by_val,
                                  'del_ind': False},
                    )

        Upload_response = list(UserRoles.objects.filter(del_ind=False).values('role', 'role_desc'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_accdata':

        for save_accdata in master_data:

            if save_accdata['del_ind']:

                AccountingData.objects.filter(account_assign_guid=save_accdata['account_assign_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(AccountingData, {
                    'account_assign_guid': save_accdata['account_assign_guid'], 'del_ind': False},
                                                                                      'accounting_data_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(AccountingData, {
                    'account_assign_guid': save_accdata['account_assign_guid'], 'del_ind': False},
                                                                                      'accounting_data_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (AccountingData.objects.filter(account_assign_guid=save_accdata['account_assign_guid'],
                                                  account_assign_value=save_accdata['account_assign_value'],
                                                  account_assign_cat=save_accdata['account_assign_cat'],
                                                  valid_from=save_accdata['valid_from'],
                                                  valid_to=save_accdata['valid_to'],
                                                  company_id=save_accdata['company_id'],
                                                  client=client).exists()):
                    continue

                elif not (AccountingData.objects.filter(account_assign_guid=save_accdata['account_assign_guid'],
                                                        account_assign_value=save_accdata['account_assign_value'],
                                                        account_assign_cat=save_accdata['account_assign_cat'],
                                                        valid_from=save_accdata['valid_from'],
                                                        valid_to=save_accdata['valid_to'],
                                                        company_id=save_accdata['company_id'],
                                                        client=client).exists()):

                    if (AccountingData.objects.filter(client=client,
                                                      account_assign_guid=save_accdata['account_assign_guid'],
                                                      account_assign_value=save_accdata['account_assign_value'],
                                                      account_assign_cat=save_accdata['account_assign_cat'],
                                                      ).exists()):
                        AccountingData.objects.filter(account_assign_guid=save_accdata['account_assign_guid'],
                                                      account_assign_value=save_accdata['account_assign_value'],
                                                      account_assign_cat=save_accdata['account_assign_cat'],
                                                      client=client).update(
                            account_assign_value=save_accdata['account_assign_value'],
                            account_assign_cat=AccountAssignmentCategory.objects.get(
                                account_assign_cat=save_accdata['account_assign_cat']),
                            valid_from=save_accdata['valid_from'],
                            valid_to=save_accdata['valid_to'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            company_id=save_accdata['company_id'],
                            accounting_data_created_at=created_time_val,
                            accounting_data_created_by=created_by_val,
                            accounting_data_changed_at=changed_at_val,
                            accounting_data_changed_by=changed_by_val
                        )


                    elif (AccountingData.objects.filter(client=client,
                                                        account_assign_value=save_accdata['account_assign_value'],
                                                        account_assign_cat=save_accdata['account_assign_cat'],
                                                        ).exists()):
                        acc_data_errmsg_unique = "'Duplicate record exists on Acc Assignment value, Assign Category and Client.'"
                        return False, acc_data_errmsg_unique

                    else:
                        AccountingData.objects.filter(account_assign_guid=save_accdata['account_assign_guid'],
                                                      #  account_assign_value=save_accdata['account_assign_value'],
                                                      # account_assign_cat=save_accdata['account_assign_cat'],
                                                      client=client).update(
                            # account_assign_guid = save_accdata['account_assign_guid'],
                            account_assign_value=save_accdata['account_assign_value'],
                            account_assign_cat=AccountAssignmentCategory.objects.get(
                                account_assign_cat=save_accdata['account_assign_cat']),
                            valid_from=save_accdata['valid_from'],
                            valid_to=save_accdata['valid_to'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            company_id=save_accdata['company_id'],
                            accounting_data_created_at=created_time_val,
                            accounting_data_created_by=created_by_val,
                            accounting_data_changed_at=changed_at_val,
                            accounting_data_changed_by=changed_by_val
                        )

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_accdata['account_assign_guid'] == 'GUID':

                    if (AccountingData.objects.filter(client=client,
                                                      account_assign_value=save_accdata['account_assign_value'],
                                                      account_assign_cat=save_accdata['account_assign_cat']
                                                      ).exists()):
                        acc_data_errmsg_unique = "'Duplicate record exists on Acc Assignment value,Acc Assign Category and Client.'"
                        return False, acc_data_errmsg_unique
                    else:
                        obj, created = AccountingData.objects.get_or_create(
                            account_assign_guid=guid_generator(),
                            del_ind=False,
                            account_assign_value=save_accdata['account_assign_value'],
                            client=OrgClients.objects.get(client=client),
                            account_assign_cat=AccountAssignmentCategory.objects.get(
                                account_assign_cat=save_accdata['account_assign_cat']),
                            company_id=save_accdata['company_id'],
                            valid_from=save_accdata['valid_from'],
                            valid_to=save_accdata['valid_to'],
                            accounting_data_created_at=created_time_val,
                            accounting_data_created_by=created_by_val,
                            accounting_data_changed_at=changed_at_val,
                            accounting_data_changed_by=changed_by_val,
                            defaults={}
                        )

        upload_data_accounting = list(
            AccountingData.objects.filter(del_ind=False).values('account_assign_guid', 'account_assign_value',
                                                                'valid_from',
                                                                'valid_to', 'account_assign_cat', 'company_id'))

        return upload_data_accounting, MSG112, MSG113

    if Table == 'upload_accdatades':

        rendered_account_data_desc = AccountingDataDesc.objects.filter(del_ind=False).values('acc_desc_guid',
                                                                                             'account_assign_value',
                                                                                             'account_assign_cat',
                                                                                             'company_id',
                                                                                             'language_id')

        for save_accdata in master_data:

            if save_accdata['del_ind']:

                AccountingDataDesc.objects.filter(acc_desc_guid=save_accdata['acc_desc_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(AccountingDataDesc, {
                    'acc_desc_guid': save_accdata['acc_desc_guid'], 'del_ind': False},
                                                                                      'accounting_data_desc_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(AccountingDataDesc, {
                    'acc_desc_guid': save_accdata['acc_desc_guid'], 'del_ind': False},
                                                                                      'accounting_data_desc_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (AccountingDataDesc.objects.filter(acc_desc_guid=save_accdata['acc_desc_guid'],
                                                      account_assign_value=save_accdata['account_assign_value'],
                                                      account_assign_cat=save_accdata['account_assign_cat'],
                                                      language_id=save_accdata['language_id'],
                                                      description=save_accdata['description'],
                                                      company_id=save_accdata['company_id'],
                                                      client=client).exists()):
                    continue

                elif not (AccountingDataDesc.objects.filter(acc_desc_guid=save_accdata['acc_desc_guid'],
                                                            account_assign_value=save_accdata['account_assign_value'],
                                                            account_assign_cat=save_accdata['account_assign_cat'],
                                                            language_id=save_accdata['language_id'],
                                                            description=save_accdata['description'],
                                                            company_id=save_accdata['company_id'],
                                                            client=client).exists()):

                    if (AccountingDataDesc.objects.filter(client=client,
                                                          account_assign_value=save_accdata['account_assign_value'],
                                                          account_assign_cat=save_accdata['account_assign_cat'],
                                                          language_id=save_accdata['language_id'],
                                                          company_id=save_accdata['company_id'],
                                                          ).exists()):
                        AccountingDataDesc.objects.filter(account_assign_value=save_accdata['account_assign_value'],
                                                          account_assign_cat=save_accdata['account_assign_cat'],
                                                          language_id=save_accdata['language_id'],
                                                          company_id=save_accdata['company_id'],
                                                          client=client).update(
                            account_assign_value=save_accdata['account_assign_value'],
                            account_assign_cat=AccountAssignmentCategory.objects.get(
                                account_assign_cat=save_accdata['account_assign_cat']),
                            language_id=save_accdata['language_id'],
                            description=save_accdata['description'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            company_id=save_accdata['company_id'],
                            accounting_data_desc_created_at=created_time_val,
                            accounting_data_desc_created_by=created_by_val,
                            accounting_data_desc_changed_at=changed_at_val,
                            accounting_data_desc_changed_by=changed_by_val
                        )

                    else:
                        save_accdata['acc_desc_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_accdata['acc_desc_guid'] == 'GUID':
                    obj, created = AccountingDataDesc.objects.get_or_create(
                        acc_desc_guid=guid_generator(),
                        account_assign_value=save_accdata['account_assign_value'],
                        account_assign_cat=AccountAssignmentCategory.objects.get(
                            account_assign_cat=save_accdata['account_assign_cat']),
                        language_id=Languages.objects.get(language_id=save_accdata['language_id']),
                        description=save_accdata['description'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        company_id=save_accdata['company_id'],
                        accounting_data_desc_created_at=created_time_val,
                        accounting_data_desc_created_by=created_by_val,
                        accounting_data_desc_changed_at=changed_at_val,
                        accounting_data_desc_changed_by=changed_by_val
                    )

        upload_data_accounting_desc = list(
            AccountingDataDesc.objects.filter(del_ind=False).values('acc_desc_guid', 'account_assign_value',
                                                                    'description',
                                                                    'account_assign_cat', 'company_id', 'language_id'))

        return (upload_data_accounting_desc, MSG112, MSG113)
        # return True,Upload_response

    if Table == 'upload_applimit':

        for save_applimit in master_data:

            if (save_applimit['del_ind'] == True):

                ApproverLimit.objects.filter(app_guid=save_applimit['app_guid']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(ApproverLimit, {
                    'app_guid': save_applimit['app_guid'], 'del_ind': False}, 'approver_limit_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(ApproverLimit, {
                    'app_guid': save_applimit['app_guid'], 'del_ind': False}, 'approver_limit_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")

                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()

                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (ApproverLimit.objects.filter(app_guid=save_applimit['app_guid'],
                                                 approver_username=save_applimit['approver_username'],
                                                 app_code_id=save_applimit['app_code_id'],
                                                 company_id=save_applimit['company_id'],
                                                 client=client).exists()):
                    continue

                elif not (ApproverLimit.objects.filter(app_guid=save_applimit['app_guid'],
                                                       approver_username=save_applimit['approver_username'],
                                                       app_code_id=save_applimit['app_code_id'],
                                                       company_id=save_applimit['company_id'],
                                                       client=client).exists()):

                    if (ApproverLimit.objects.filter(client=client,
                                                     app_code_id=save_applimit['app_code_id'],
                                                     company_id=save_applimit['company_id'],
                                                     ).exists()):
                        ApproverLimit.objects.filter(app_code_id=save_applimit['app_code_id'],
                                                     company_id=save_applimit['company_id'],
                                                     client=client).update(
                            approver_username=save_applimit['approver_username'],
                            app_code_id=save_applimit['app_code_id'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            company_id=save_applimit['company_id'],
                            approver_limit_created_at=created_time_val,
                            approver_limit_created_by=created_by_val,
                            approver_limit_changed_at=changed_at_val,
                            approver_limit_changed_by=changed_by_val,
                        )

                    else:
                        save_applimit['app_guid'] = 'GUID'
                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_applimit['app_guid'] == 'GUID':
                    obj, created = ApproverLimit.objects.get_or_create(
                        app_guid=guid_generator(),
                        approver_username=save_applimit['approver_username'],
                        app_code_id=save_applimit['app_code_id'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        company_id=save_applimit['company_id'],
                        approver_limit_created_at=created_time_val,
                        approver_limit_created_by=created_by_val,
                        approver_limit_changed_at=changed_at_val,
                        approver_limit_changed_by=changed_by_val
                    )

        upload_applimit = list(
            ApproverLimit.objects.filter(client=client, del_ind=False).values('app_guid', 'approver_username',
                                                                              'app_code_id', 'company_id'))

        return upload_applimit, MSG112, MSG113

    if Table == 'upload_applimval':

        for save_applimval in master_data:

            if (save_applimval['del_ind'] == True):

                ApproverLimitValue.objects.filter(app_lim_dec_guid=save_applimval['app_lim_dec_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(ApproverLimitValue, {
                    'app_lim_dec_guid': save_applimval['app_lim_dec_guid'], 'del_ind': False},
                                                                                      'approver_limit_value_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(ApproverLimitValue, {
                    'app_lim_dec_guid': save_applimval['app_lim_dec_guid'], 'del_ind': False},
                                                                                      'approver_limit_value_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (ApproverLimitValue.objects.filter(app_lim_dec_guid=save_applimval['app_lim_dec_guid'],
                                                      app_types=save_applimval['app_types'],
                                                      app_code_id=save_applimval['app_code_id'],
                                                      upper_limit_value=save_applimval['upper_limit_value'],
                                                      currency_id=save_applimval['currency_id'],
                                                      company_id=save_applimval['company_id'],
                                                      client=client).exists()):
                    continue

                elif not (ApproverLimitValue.objects.filter(app_lim_dec_guid=save_applimval['app_lim_dec_guid'],
                                                            app_types=save_applimval['app_types'],
                                                            app_code_id=save_applimval['app_code_id'],
                                                            upper_limit_value=save_applimval['upper_limit_value'],
                                                            currency_id=save_applimval['currency_id'],
                                                            company_id=save_applimval['company_id'],
                                                            client=client).exists()):

                    if (ApproverLimitValue.objects.filter(client=client,
                                                          app_types=save_applimval['app_types'],
                                                          app_code_id=save_applimval['app_code_id'],
                                                          company_id=save_applimval['company_id']
                                                          ).exists()):
                        ApproverLimitValue.objects.filter(app_types=save_applimval['app_types'],
                                                          app_code_id=save_applimval['app_code_id'],
                                                          company_id=save_applimval['company_id'],
                                                          client=client).update(
                            upper_limit_value=save_applimval['upper_limit_value'],
                            app_code_id=save_applimval['app_code_id'],
                            del_ind=False,
                            app_types=ApproverType.objects.get(app_types=save_applimval['app_types']),
                            client=OrgClients.objects.get(client=client),
                            currency_id=save_applimval['currency_id'],
                            company_id=save_applimval['company_id'],
                            approver_limit_value_created_at=created_time_val,
                            approver_limit_value_created_by=created_by_val,
                            approver_limit_value_changed_at=changed_at_val,
                            approver_limit_value_changed_by=changed_by_val
                        )
                    else:
                        save_applimval['app_lim_dec_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_applimval['app_lim_dec_guid'] == 'GUID':
                    obj, created = ApproverLimitValue.objects.get_or_create(
                        app_lim_dec_guid=guid_generator(),
                        upper_limit_value=save_applimval['upper_limit_value'],
                        app_code_id=save_applimval['app_code_id'],
                        app_types
                        =ApproverType.objects.get(app_types=save_applimval['app_types']),
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        currency_id=Currency.objects.get(currency_id=save_applimval['currency_id']),
                        company_id=save_applimval['company_id'],
                        approver_limit_value_created_at=created_time_val,
                        approver_limit_value_created_by=created_by_val,
                        approver_limit_value_changed_at=changed_at_val,
                        approver_limit_value_changed_by=changed_by_val
                    )

        upload_applimval = list(
            ApproverLimitValue.objects.filter(client=client, del_ind=False).values('app_lim_dec_guid', 'app_types',
                                                                                   'app_code_id', 'currency_id',
                                                                                   'upper_limit_value', 'company_id'))
        return upload_applimval, MSG112, MSG113

    if Table == 'upload_spndlimid':
        for save_spndlimid in master_data:
            if save_spndlimid['del_ind']:
                SpendLimitId.objects.filter(spend_guid=save_spndlimid['spend_guid']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(SpendLimitId, {
                    'spend_guid': save_spndlimid['spend_guid'], 'del_ind': False}, 'spend_limit_id_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(SpendLimitId, {
                    'spend_guid': save_spndlimid['spend_guid'], 'del_ind': False}, 'spend_limit_id_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (SpendLimitId.objects.filter(spend_guid=save_spndlimid['spend_guid'],
                                                spender_username=save_spndlimid['spender_username'],
                                                spend_code_id=save_spndlimid['spend_code_id'],
                                                company_id=save_spndlimid['company_id'],
                                                client=client).exists()):
                    continue

                elif not (SpendLimitId.objects.filter(spend_guid=save_spndlimid['spend_guid'],
                                                      spender_username=save_spndlimid['spender_username'],
                                                      spend_code_id=save_spndlimid['spend_code_id'],
                                                      company_id=save_spndlimid['company_id'],
                                                      client=client).exists()):

                    if (SpendLimitId.objects.filter(client=client,
                                                    company_id=save_spndlimid['company_id'],
                                                    ).exists()):
                        SpendLimitId.objects.filter(company_id=save_spndlimid['company_id'],
                                                    client=client).update(
                            spender_username=save_spndlimid['spender_username'],
                            spend_code_id=save_spndlimid['spend_code_id'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            company_id=save_spndlimid['company_id'],
                            spend_limit_id_created_at=created_time_val,
                            spend_limit_id_created_by=created_by_val,
                            spend_limit_id_changed_at=changed_at_val,
                            spend_limit_id_changed_by=changed_by_val,
                        )

                    else:
                        save_spndlimid['spend_guid'] = 'GUID'
                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_spndlimid['spend_guid'] == 'GUID':
                    obj, created = SpendLimitId.objects.get_or_create(
                        spend_guid=guid_generator(),
                        spender_username=save_spndlimid['spender_username'],
                        spend_code_id=save_spndlimid['spend_code_id'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        company_id=save_spndlimid['company_id'],
                        spend_limit_id_created_at=created_time_val,
                        spend_limit_id_created_by=created_by_val,
                        spend_limit_id_changed_at=changed_at_val,
                        spend_limit_id_changed_by=changed_by_val
                    )

            upload_spndlimid = list(
                SpendLimitId.objects.filter(client=client, del_ind=False).values('spend_guid', 'spender_username',
                                                                                 'spend_code_id', 'company_id'))

        return upload_spndlimid, MSG112, MSG113

    if Table == 'upload_spndlimval':

        Success_message = "'Data Saved Successfully'"

        spndlimval_not_exist: object = SpendLimitValue.objects.filter(del_ind=False).exclude \
            (spend_lim_value_guid__in=[spndlimval['spend_lim_value_guid'] for spndlimval in master_data])

        for set_del_int in spndlimval_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_spndlimval in master_data:
            created_at_val = django_query_instance.django_filter_value_list_query(SpendLimitValue, {
                'spend_lim_value_guid': save_spndlimval['spend_lim_value_guid'], 'del_ind': False},
                                                                                  'spend_limit_value_created_at')
            created_by_val = django_query_instance.django_filter_value_list_query(SpendLimitValue, {
                'spend_lim_value_guid': save_spndlimval['spend_lim_value_guid'], 'del_ind': False},
                                                                                  'spend_limit_value_created_by')

            if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                changed_at_val = datetime.today().date()
                changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                created_by_val = created_by_val[0]
            else:
                created_time_val = datetime.today().date()
                changed_at_val = None
                changed_by_val = None
                created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip the record
            if (SpendLimitValue.objects.filter(spend_lim_value_guid=save_spndlimval['spend_lim_value_guid'],
                                               upper_limit_value=save_spndlimval['upper_limit_value'],
                                               spend_code_id=save_spndlimval['spend_code_id'],
                                               currency_id=save_spndlimval['currency_id'],
                                               company_id=save_spndlimval['company_id'],
                                               client=client).exists()):
                continue

            elif not (SpendLimitValue.objects.filter(spend_lim_value_guid=save_spndlimval['spend_lim_value_guid'],
                                                     upper_limit_value=save_spndlimval['upper_limit_value'],
                                                     spend_code_id=save_spndlimval['spend_code_id'],
                                                     currency_id=save_spndlimval['currency_id'],
                                                     company_id=save_spndlimval['company_id'],
                                                     client=client).exists()):

                if (SpendLimitValue.objects.filter(client=client,
                                                   spend_lim_value_guid=save_spndlimval['spend_lim_value_guid'],
                                                   ).exists()):
                    SpendLimitValue.objects.filter(spend_lim_value_guid=save_spndlimval['spend_lim_value_guid'],
                                                   client=client).update(
                        upper_limit_value=save_spndlimval['upper_limit_value'],
                        spend_code_id=save_spndlimval['spend_code_id'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        currency_id=save_spndlimval['currency_id'],
                        company_id=save_spndlimval['company_id'],
                        spend_limit_value_created_at=created_time_val,
                        spend_limit_value_created_by=created_by_val,
                        spend_limit_value_changed_at=changed_at_val,
                        spend_limit_value_changed_by=changed_by_val
                    )

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

            if save_spndlimval['spend_lim_value_guid'] == 'GUID':
                obj, created = SpendLimitValue.objects.get_or_create(
                    spend_lim_value_guid=guid_generator(),
                    upper_limit_value=save_spndlimval['upper_limit_value'],
                    spend_code_id=save_spndlimval['spend_code_id'],
                    del_ind=False,
                    client=OrgClients.objects.get(client=client),
                    currency_id=Currency.objects.get(currency_id=save_spndlimval['currency_id']),
                    company_id=save_spndlimval['company_id'],
                    spend_limit_value_created_at=created_time_val,
                    spend_limit_value_created_by=created_by_val,
                    spend_limit_value_changed_at=changed_at_val,
                    spend_limit_value_changed_by=changed_by_val
                )

        return True, Success_message

    if Table == 'upload_wfschema':

        Success_message = MSG037

        wfschema_not_exist: object = WorkflowSchema.objects.filter(del_ind=False).exclude \
            (workflow_schema_guid__in=[wfschema['workflow_schema_guid'] for wfschema in master_data])

        for set_del_int in wfschema_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_wfschema in master_data:
            created_at_val = django_query_instance.django_filter_value_list_query(WorkflowSchema, {
                'workflow_schema_guid': save_wfschema['workflow_schema_guid'], 'del_ind': False},
                                                                                  'workflow_schema_created_at')
            created_by_val = django_query_instance.django_filter_value_list_query(WorkflowSchema, {
                'workflow_schema_guid': save_wfschema['workflow_schema_guid'], 'del_ind': False},
                                                                                  'workflow_schema_created_by')

            if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                changed_at_val = datetime.today().date()
                changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                created_by_val = created_by_val[0]
            else:
                created_time_val = datetime.today().date()
                changed_at_val = None
                changed_by_val = None
                created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip the record
            if (WorkflowSchema.objects.filter(workflow_schema_guid=save_wfschema['workflow_schema_guid'],
                                              workflow_schema=save_wfschema['workflow_schema'],
                                              app_types=save_wfschema['app_types'],
                                              company_id=save_wfschema['company_id'],
                                              client=client).exists()):
                continue

            elif not (WorkflowSchema.objects.filter(workflow_schema_guid=save_wfschema['workflow_schema_guid'],
                                                    workflow_schema=save_wfschema['workflow_schema'],
                                                    app_types=save_wfschema['app_types'],
                                                    company_id=save_wfschema['company_id'],
                                                    client=client).exists()):

                if (WorkflowSchema.objects.filter(client=client,
                                                  workflow_schema_guid=save_wfschema['workflow_schema_guid'],
                                                  ).exists()):
                    WorkflowSchema.objects.filter(workflow_schema_guid=save_wfschema['workflow_schema_guid'],
                                                  client=client).update(
                        workflow_schema=save_wfschema['workflow_schema'],
                        app_types=ApproverType.objects.get(app_types=save_wfschema['app_types']),
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        company_id=save_wfschema['company_id'],
                        workflow_schema_created_at=created_time_val,
                        workflow_schema_created_by=created_by_val,
                        workflow_schema_changed_at=changed_at_val,
                        workflow_schema_changed_by=changed_by_val
                    )

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

            if save_wfschema['workflow_schema_guid'] == 'GUID':
                obj, created = WorkflowSchema.objects.get_or_create(
                    workflow_schema_guid=guid_generator(),
                    workflow_schema=save_wfschema['workflow_schema'],
                    app_types=ApproverType.objects.get(app_types=save_wfschema['app_types']),
                    del_ind=False,
                    client=OrgClients.objects.get(client=client),
                    company_id=save_wfschema['company_id'],
                    workflow_schema_created_at=created_time_val,
                    workflow_schema_created_by=created_by_val,
                    workflow_schema_changed_at=changed_at_val,
                    workflow_schema_changed_by=changed_by_val
                )

        return True, Success_message

    if Table == 'upload_WFACC':

        Success_message = MSG037

        wfacc_not_exist: object = WorkflowACC.objects.filter(del_ind=False).exclude \
            (workflow_acc_guid__in=[wfacc['workflow_acc_guid'] for wfacc in master_data])

        for set_del_int in wfacc_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_wfacc in master_data:
            created_at_val = django_query_instance.django_filter_value_list_query(WorkflowACC, {
                'workflow_acc_guid': save_wfacc['workflow_acc_guid'], 'del_ind': False},
                                                                                  'workflow_acc_created_at')
            created_by_val = django_query_instance.django_filter_value_list_query(WorkflowACC, {
                'workflow_acc_guid': save_wfacc['workflow_acc_guid'], 'del_ind': False},
                                                                                  'workflow_acc_created_by')

            if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")

                changed_at_val = datetime.today().date()
                changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                created_by_val = created_by_val[0]
            else:
                created_time_val = datetime.today().date()

                changed_at_val = None
                changed_by_val = None
                created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip the record
            if (WorkflowACC.objects.filter(workflow_acc_guid=save_wfacc['workflow_acc_guid'],
                                           app_username=save_wfacc['app_username'],
                                           acc_value=save_wfacc['acc_value'],
                                           sup_acc_value=save_wfacc['sup_acc_value'],
                                           account_assign_cat=save_wfacc['account_assign_cat'],
                                           sup_account_assign_cat=save_wfacc['sup_account_assign_cat'],
                                           company_id=save_wfacc['company_id'],
                                           sup_company_id=save_wfacc['sup_company_id'],
                                           currency_id=save_wfacc['currency_id'],
                                           client=client, del_ind=False).exits()):
                continue

            elif not (WorkflowACC.objects.filtr(workflow_acc_gid=save_wfacc['workflow_acc_guid'],
                                                app_username=save_wfacc['app_username'],
                                                acc_value=save_wfacc['acc_value'],
                                                sup_acc_value=save_wfacc['sup_acc_value'],
                                                account_assign_at=save_wfacc['account_assign_cat'],
                                                sup_account_assign_at=save_wfacc['sup_account_assign_cat'],
                                                company_id=save_wfacc['company_id'],
                                                sup_company_id=save_wfacc['sup_company_id'],
                                                currency_id=save_wfacc['currency_id'],
                                                client=client, del_id=False).exts()):

                if (WorkflowACC.objects.fier(client=client,
                                             workflow_acc_guid=save_wfacc['workflow_acc_guid'],
                                             ).exts()):
                    WorkflowACC.objects.fier(workflow_acc_guid=save_wfacc['workflow_acc_guid'],
                                             client=client).upte(
                        app_username=save_wfacc['app_username'],
                        acc_value=save_wfacc['acc_value'],
                        sup_acc_value=save_wfacc['sup_acc_value'],
                        account_assign_cat=AccountAssignmentCategory.objects.get
                        (account_assign_cat=save_wfacc['account_assign_cat']),
                        sup_account_assign_cat=AccountAssignmentCategory.objects.get
                        (account_assign_cat=save_wfacc['sup_account_assign_cat']),
                        company_id=save_wfacc['company_id'],
                        sup_company_id=save_wfacc['sup_company_id'],
                        currency_id=Currency.objects.gt(currency_id=save_wfacc['currenc_d']),
                        client=OrgClients.objects.get(client=client),
                        workflow_acc_created_at=created_time_val,
                        workflow_acc_created_by=created_by_val,
                        workflow_acc_changed_at=changed_at_val,
                        workflow_acc_changed_by=changed_by_val,
                        del_ind=False)

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

            if save_wfacc['workflow_acc_guid'] == 'GUID':
                obj, created = WorkflowACC.objects.get_or_create(
                    workflow_acc_guid=guid_generator(),
                    app_username=save_wfacc['app_username'],
                    acc_value=save_wfacc['acc_value'],
                    sup_acc_value=save_wfacc['sup_acc_value'],
                    account_assign_cat=AccountAssignmentCategory.objects.get
                    (account_assign_cat=save_wfacc['account_assign_cat']),
                    sup_account_assign_cat=AccountAssignmentCategory.objects.get(
                        account_assign_cat=save_wfacc['sup_account_assign_cat']),
                    company_id=save_wfacc['company_id'],
                    sup_company_id=save_wfacc['sup_company_id'],
                    currency_id=Currency.objects.get(currency_id=save_wfacc['currency_id']),
                    client=OrgClients.objects.get(client=client),
                    workflow_acc_created_at=created_time_val,
                    workflow_acc_created_by=created_by_val,
                    workflow_acc_changed_at=changed_at_val,
                    workflow_acc_changed_by=changed_by_val,
                    del_ind=False)
        return True, Success_message

    if Table == 'upload_orgnodetypes':

        orgnodetypes_not_exist: object = OrgNodeTypes.objects.filter(del_ind=False).exclude \
            (node_type_guid__in=[orgnodetypes['node_type_guid'] for orgnodetypes in master_data])

        for save_orgnodetypes in master_data:
            if save_orgnodetypes['del_ind']:

                OrgNodeTypes.objects.filter(node_type_guid=save_orgnodetypes['node_type_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(OrgNodeTypes, {
                    'node_type_guid': save_orgnodetypes['node_type_guid'], 'del_ind': False},
                                                                                      'org_node_types_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(OrgNodeTypes, {
                    'node_type_guid': save_orgnodetypes['node_type_guid'], 'del_ind': False},
                                                                                      'org_node_types_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (OrgNodeTypes.objects.filter(node_type_guid=save_orgnodetypes['node_type_guid'],
                                                node_type=save_orgnodetypes['node_type'],
                                                description=save_orgnodetypes['description'],
                                                client=client).exists()):
                    continue

                elif not (OrgNodeTypes.objects.filter(node_type_guid=save_orgnodetypes['node_type_guid'],
                                                      node_type=save_orgnodetypes['node_type'],
                                                      description=save_orgnodetypes['description'],
                                                      client=client).exists()):

                    if (OrgNodeTypes.objects.filter(client=client,
                                                    node_type=save_orgnodetypes['node_type'],
                                                    ).exists()):
                        OrgNodeTypes.objects.filter(node_type=save_orgnodetypes['node_type'],
                                                    client=client).update(
                            node_type=save_orgnodetypes['node_type'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            description=save_orgnodetypes['description'],
                            org_node_types_created_at=created_time_val,
                            org_node_types_created_by=created_by_val,
                            org_node_types_changed_at=changed_at_val,
                            org_node_types_changed_by=changed_by_val
                        )

                    else:
                        save_orgnodetypes['node_type_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_orgnodetypes['node_type_guid'] == 'GUID':
                    obj, created = OrgNodeTypes.objects.get_or_create(
                        node_type_guid=guid_generator(),
                        node_type=save_orgnodetypes['node_type'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        description=save_orgnodetypes['description'],
                        org_node_types_created_at=created_time_val,
                        org_node_types_created_by=created_by_val,
                        org_node_types_changed_at=changed_at_val,
                        org_node_types_changed_by=changed_by_val
                    )

        Upload_response = list(OrgNodeTypes.objects.filter(del_ind=False).values('node_type', 'description'))
        return Upload_response, MSG112, MSG113

    if Table == 'upload_orgattributes':

        Success_message = MSG037

        OrgAttrib_not_exist: object = OrgAttributes.objects.filter(del_ind=False).exclude \
            (attribute_id__in=[OrgAttrib['attribute_id'] for OrgAttrib in master_data])

        for save_OrgAttrib in master_data:
            if save_OrgAttrib['del_ind']:

                OrgNodeTypes.objects.filter(attribute_id=save_OrgAttrib['attribute_id']).update(
                    del_ind=True)
            else:

                if save_OrgAttrib['range_indicator'] == 'YES':
                    save_OrgAttrib['range_indicator'] = True
                elif save_OrgAttrib['range_indicator'] == 'NO':
                    save_OrgAttrib['range_indicator'] = False

                if save_OrgAttrib['multiple_value'] == 'YES':
                    save_OrgAttrib['multiple_value'] = True
                elif save_OrgAttrib['multiple_value'] == 'NO':
                    save_OrgAttrib['multiple_value'] = False

                if save_OrgAttrib['allow_defaults'] == 'YES':
                    save_OrgAttrib['allow_defaults'] = True
                elif save_OrgAttrib['allow_defaults'] == 'NO':
                    save_OrgAttrib['allow_defaults'] = False

                if save_OrgAttrib['inherit_values'] == 'YES':
                    save_OrgAttrib['inherit_values'] = True
                elif save_OrgAttrib['inherit_values'] == 'NO':
                    save_OrgAttrib['inherit_values'] = False

                created_at_val = django_query_instance.django_filter_value_list_query(OrgAttributes, {
                    'attribute_id': save_OrgAttrib['attribute_id'], 'del_ind': False},
                                                                                      'org_attributes_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(OrgAttributes, {
                    'attribute_id': save_OrgAttrib['attribute_id'], 'del_ind': False},
                                                                                      'org_attributes_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (OrgAttributes.objects.filter(attribute_id=save_OrgAttrib['attribute_id'],
                                                 attribute_name=save_OrgAttrib['attribute_name'],
                                                 range_indicator=save_OrgAttrib['range_indicator'],
                                                 multiple_value=save_OrgAttrib['multiple_value'],
                                                 allow_defaults=save_OrgAttrib['allow_defaults'],
                                                 inherit_values=save_OrgAttrib['inherit_values'],
                                                 maximum_length=save_OrgAttrib['maximum_length'],
                                                 del_ind=False).exists()):
                    continue

                elif not (OrgAttributes.objects.filter(attribute_id=save_OrgAttrib['attribute_id'],
                                                       attribute_name=save_OrgAttrib['attribute_name'],
                                                       range_indicator=save_OrgAttrib['range_indicator'],
                                                       multiple_value=save_OrgAttrib['multiple_value'],
                                                       allow_defaults=save_OrgAttrib['allow_defaults'],
                                                       inher_vues=save_OrgAttrib['inherit_values'],
                                                       maximmlnth=save_OrgAttrib['maximum_length'],
                                                       delind=False).eists()):

                    if (OrgAttributes.objets.fler(attribute_id=save_OrgAttrib['attribute_id'],
                                                  ).eists()):
                        OrgAttributes.objcs.fler(attribute_id=save_OrgAttrib['attribute_id']
                                                 ).udate(
                            abtee=save_OrgAttrib['attribute_name'],
                            range_or=save_OrgAttrib['range_indicator'],
                            multiaue=save_OrgAttrib['multiple_value'],
                            a_defs=save_OrgAttrib['allowdefalts'],
                            ii_vs=save_OrgAttrib['inherit_values'],
                            mau_lth=save_OrgAttrib['maximum_length'],
                            org_attributes_created_at=created_time_val,
                            org_attributes_created_by=created_by_val,
                            org_attributes_changed_at=changed_at_val,
                            org_attributes_changed_by=changed_by_val,
                            de_id=False)

                    else:
                        # Below logic is for new records added.
                        # The GUID will be hardcoded to GUID from UI and sent to backend.
                        obj, created = OrgAttributes.objects.get_or_create(
                            attribute_id=save_OrgAttrib['attribute_id'],
                            attribute_name=save_OrgAttrib['attribute_name'],
                            range_indicator=save_OrgAttrib['range_indicator'],
                            multiple_value=save_OrgAttrib['multiple_value'],
                            allow_defaults=save_OrgAttrib['allow_defaults'],
                            inherit_values=save_OrgAttrib['inherit_values'],
                            maximum_length=save_OrgAttrib['maximum_length'],
                            org_attributes_created_at=created_time_val,
                            org_attributes_created_by=created_by_val,
                            org_attributes_changed_at=changed_at_val,
                            org_attributes_changed_by=changed_by_val,
                            del_ind=False)

        Upload_response = list(OrgAttributes.objects.filter(del_ind=False).values('attribute_id', 'attribute_name',
                                                                                  'range_indicator', 'multiple_value',
                                                                                  'allow_defaults', 'inherit_values',
                                                                                  'maximum_length'))
        return Upload_response, MSG112, MSG113

    if Table == 'upload_companies':

        Success_message = MSG037

        orgcompanies_not_exist: object = OrgCompanies.objets.flter(delind=False).exclude \
            (company_guid__in=[orgcompanies['company_guid'] for orgcompanies in master_data])

        for set_del_int in orgcompanies_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_orgcompanies in master_data:

            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip the record
            if (OrgCompanies.objects.filter(company_guid=save_orgcompanies['company_guid'],
                                            company_id=save_orgcompanies['company_id'],
                                            name1=save_orgcompanies['name1'],
                                            name2=save_orgcompanies['name2'],
                                            object_id=save_orgcompanies['object_id'],
                                            del_ind=False,
                                            client=client).exists()):
                continue

            elif not (OrgCompanies.objets.filter(company_guid=save_orgcompanies['company_guid'],
                                                 company_id=save_orgcompanies['company_id'],
                                                 name1=save_orgcompanies['name1'],
                                                 name2=save_orgcompanies['name2'],
                                                 object_id=save_orgcompanies['object_id'],
                                                 del_ind=False,
                                                 cint=client).exists()):

                if (OrgCompanies.obes.filter(client=client,
                                             company_guid=save_orgcompanies['company_guid'],
                                             ).exists()):
                    OrgCompanies.ojs.filter(company_guid=save_orgcompanies['company_guid'],
                                            cent=client).update(company_id=save_orgcompanies['company_id'],
                                                                name1=save_orgcompanies['name1'],
                                                                name2=save_orgcompanies['name2'],
                                                                object_id=OrgModel.
                                                                objects.get(object_id=save_orgcompanies['object_id']),
                                                                del_ind=False,
                                                                client=OrgClients.objects.get(client=client))

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

            if save_orgcompanies['company_guid'] == 'GUID':
                obj, created = OrgCompanies.objects.get_or_create(
                    company_guid=guid_generator(),
                    company_id=save_orgcompanies['company_id'],
                    name1=save_orgcompanies['name1'],
                    name2=save_orgcompanies['name2'],
                    object_id=OrgModel.ojecs.get(object_id=save_orgcompanies['object_id']),
                    del_ind=False,
                    client=OrgClients.objects.get(client=client))

        return True, Success_message

    if Table == 'upload_porg':

        Success_message = MSG037

        orgporg_not_exist: object = OrgPorg.objects.filer(del_ind=False).exclude \
            (porg_guid__in=[orgporg['porg_uid'] for

                            orgporg in master_data])

        for set_del_int in orgporg_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_orgporg in master_data:

            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip therrd
            if (OrgPorg.objects.flter(porg_guid=save_orgporg['porg_guid']
                    ,
                                      pogid=save_orgporg['porg_id'],
                                      copyid=save_orgporg['company_id'],
                                      deciton=save_orgporg['description'],
                                      objetid=save_orgporg['object_id'],
                                      del_ind=False,
                                      client=client).eists()):
                continue

            elif not (OrgPorg.objects.
                    fler(porg_guid=save_orgporg[
                'porg_guid'],
                         porg_id=save_orgporg['porg_id'],
                         company_id=save_orgporg['company_id'],
                         description=save_orgporg['description'],
                         object_id=save_orgporg['objc_id'],
                         del_ind=False,
                         client=client).eists()):

                if (OrgPorg.objects.fler(client=client,
                                         porg_guid=save_orgporg['porg_guid'
                                         ],
                                         ).eists()):
                    OrgPorg.objects.fler(porg_guid=save_orgporg['porg_gud'],
                                         client=client).udate(
                        compayid=save_orgporg['company_id'],
                        descriton=save_orgporg['description'],
                        pgid=

                        save_orgporg['porg_id'],
                        object_id=OrgModel.objects.get(object_id=save_orgporg['objet_id']),
                        del_ind=False,
                        client=OrgClients.objecs.get(client=client))

            # Below logic isfor new records added. The GUIDwll be hardcoded to GUID from UI and sent to backend.

            if save_orgporg['porg_guid'] == 'GUID':
                obj, created = OrgPorg.objects.get_o_create(
                    porg_guid=guid_generator(),
                    porg_id=save_orgporg['porg_id'],
                    company_id=save_orgporg['company_id'],
                    description=save_orgporg['description'],
                    object_id=OrgModel.objects.get(object_id=save_orgporg['object_id']), del_ind=False
                    , client=OrgClients.objects.get(client=client
                                                    ))

        return True, Success_message

    if Table == 'upload_pgrp':

        Success_message = MSG037

        orggrp_not_exist: object = OrgPGroup.objects.filter(del_ind=False).exclde \
            (pgroup_guid__in=[orggrp['pgroup_guid'] for orggrp in master_data])

        for set_del_int in orggrp_not_exist:
            set_del_int.del_ind = True
            set_del_int.sae()

        for save_orggrp in master_data: \
                # Belwlogic is for existing e cords changed.

            # Check if there is any change in the record if no then skip the record
            if (OrgPGroup.objects.filter(pgroup_guid=save_orggrp['pgroup_guid'],
                                         porg_id=save_orggrp['porg_id'], pgroup_id=save_orggrp['pgroup_id'],
                                         description=save_orggrp[
                                             'description'], object_id=save_orggrp['object_id'],
                                         del_ind=False,
                                         client=client).exists()):
                continue

            elif not (OrgPGroup.objects.filter(pgroup_guid=save_orggrp['pgrou_uid'],
                                               porg_id=save_orggrp['porg_id'],
                                               pgroup_id=save_orggrp['pgroup_id'
                                               ],
                                               description=save_orggrp['description'],
                                               object_id=save_orggrp['object_id'],
                                               del_ind=False,
                                               client=client).exists()):

                if (OrgPGroup.objects.filter(client=client,
                                             pgroup_guid=save_orggrp['pgroup_guid'],
                                             ).exists()):
                    OrgPGroup.objects.filter(pgroup_guid=save_orggrp['pgroup_guid'],
                                             clint=client).update(
                        pgroup_id=save_orggrp['pgroup_id'],
                        description=save_orggrp['description'],
                        porg_id=save_orggrp['porg_id'],
                        object_id=OrgModel.objects.get(object_id=save_orggrp['object_id']),
                        del_ind=False,
                        client=OrgClients.objects.get(client=client))

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

            if save_orggrp['pgroup_guid'] == 'GUID':
                obj, created = OrgPGroup.ojects.get_or_create(
                    pgroupguid=guid_generator(),
                    porg_id=save_orggrp['porg_id'],
                    pgroup_id=save_orggrp['pgroup_id'],
                    description=save_orggrp['description'],
                    object_id=OrgModel.obects.get(object_id=save_orggrp['object_id']),
                    del_ind=False,
                    client=OrgClients.objecs.get(client=client))

        return True, Success_message

    if Table == 'upload_authobj':

        for save_authobj in master_data:
            if save_authobj['del_ind']:

                AuthorizationObject.objects.filter(auth_obj_id=save_authobj['auth_obj_id']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(AuthorizationObject, {
                    'auth_obj_id': save_authobj['auth_obj_id'], 'del_ind': False},
                                                                                      'authorization_object_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(AuthorizationObject, {
                    'auth_obj_id': save_authobj['auth_obj_id'], 'del_ind': False},
                                                                                      'authorization_object_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                if not (AuthorizationObject.objects.filter(auth_obj_id=save_authobj['auth_obj_id'],
                                                           auth_level=save_authobj['auth_level'],
                                                           auth_level_ID=save_authobj['auth_level_ID'],
                                                           auth_level_desc=save_authobj['auth_level_desc'],
                                                           de_ind=False).exists()):
                    obj, created = AuthorizationObject.objects.update_or_create(auth_obj_id=save_authobj['auth_obj_id'],
                                                                                defaults={'auth_obj_id': save_authobj
                                                                                ['auth_obj_id'],
                                                                                          'auth_evel': save_authobj
                                                                                          ['auth_level'],
                                                                                          'auth_lel_ID': save_authobj
                                                                                          ['auth_level_ID'],
                                                                                          'auth_level_desc':
                                                                                              save_authobj
                                                                                              ['auth_level_desc'],
                                                                                          'authorization_object_created_at': created_time_val,
                                                                                          'authorization_object_created_by': created_by_val,
                                                                                          'authorization_object_changed_at': changed_at_val,
                                                                                          'authorization_object_changed_by': changed_by_val,
                                                                                          'del_ind': False})

        Upload_response = list \
            (AuthorizationObject.objects.filter(del_ind=False).values('auth_obj_id', 'auth_leve', 'auth_level_ID',
                                                                      'auth_level_desc'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_authgrp':

        for save_authgrp in master_data:

            if (save_authgrp['del_ind'] == True):

                AuthorizationGroup.objects.filter(auth_grp_guid=save_authgrp['auth_grp_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(AuthorizationGroup, {
                    'auth_grp_guid': save_authgrp['auth_grp_guid'], 'del_ind': False},
                                                                                      'authorization_group_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(AuthorizationGroup, {
                    'auth_grp_guid': save_authgrp['auth_grp_guid'], 'del_ind': False},
                                                                                      'authorization_group_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (AuthorizationGroup.objects.filter(auth_grp_guid=save_authgrp['auth_grp_guid'],
                                                      auth_level=save_authgrp['auth_level'],
                                                      auth_obj_grp=save_authgrp['auth_obj_grp'],
                                                      auth_grp_desc=save_authgrp['auth_grp_desc'],
                                                      auth_obj_id=save_authgrp['auth_obj_id'],
                                                      de_ind=False).exists()):
                    continue

                elif not (AuthorizationGroup.objects.filter(auth_grp_guid=save_authgrp['auth_grp_guid'],
                                                            auth_level=save_authgrp['auth_level'],
                                                            auth_obj_grp=save_authgrp['auth_obj_grp'],
                                                            auth_grp_desc=save_authgrp['auth_grp_desc'],
                                                            auth_obj_id=save_authgrp['auth_obj_id'],
                                                            dl_ind=False).exists()):

                    if (AuthorizationGroup.objects.filter(auth_grp_guid=save_authgrp['auth_grp_guid'],
                                                          auth_level=save_authgrp['auth_level']
                                                          ).exists()):
                        AuthorizationGroup.objects.filter(auth_grp_guid=save_authgrp['auth_grp_guid'],
                                                          auth_level=save_authgrp['auth_level']
                                                          ).update(
                            auth_obj_grp=save_authgrp['auth_obj_grp'],
                            auth_grp_desc=save_authgrp['auth_grp_desc'],
                            auth_level=save_authgrp['auth_level'],
                            auth_obj_id=AuthorizationObject.objects.get(auth_obj_id=save_authgrp['auth_obj_id']),
                            authorization_group_created_at=created_time_val,
                            authorization_group_created_by=created_by_val,
                            authorization_group_changed_at=changed_at_val,
                            authorization_group_changed_by=changed_by_val,
                            del_ind=False)

                    else:
                        save_authgrp['auth_grp_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_authgrp['auth_grp_guid'] == 'GUID':
                    obj, created = AuthorizationGroup.objects.get_or_create(
                        auth_grp_guid=guid_generator(),
                        auth_level=save_authgrp['auth_level'],
                        auth_obj_grp=save_authgrp['auth_obj_gr'],
                        auth_grp_desc=save_authgrp['auth_grp_ec'],
                        auth_obj_id=AuthorizationGroup.objects.get(auth_obj_id=save_authgrp['auth_obj_id']),
                        authorization_group_created_at=created_time_val,
                        authorization_group_created_by=created_by_val,
                        authorization_group_changed_at=changed_at_val,
                        authorization_group_changed_by=changed_by_val,
                        del_ind=False)

        Upload_response = list(
            AuthorizationGroup.objects.filter(del_ind=False).values('auth_grp_guid', 'auth_obj_grp', 'auth_obj_id',
                                                                    'auth_grp_desc', 'auth_level'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_auth':

        for save_auth in master_data:

            if (save_auth['del_ind'] == True):

                Authorization.objects.filter(auth_guid=save_auth['auth_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Authorization, {
                    'auth_guid': save_auth['auth_guid'], 'del_ind': False},
                                                                                      'authorization_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(Authorization, {
                    'auth_guid': save_auth['auth_guid'], 'del_ind': False},
                                                                                      'authorization_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                # Below logic is for existing records changed.
                # Check if there is any change in the record if no then skip the record
                if (Authorization.objects.filter(auth_guid=save_auth['auth_guid'],
                                                 auth_obj_grp=save_auth['auth_obj_grp'],
                                                 auth_type=save_auth['auth_type'],
                                                 role=UserRoles.objects.get(role=save_auth['role']),
                                                 del_ind=False,
                                                 client=client).exists()):
                    continue

                elif not (Authorization.objects.filter(auth_guid=save_auth['auth_guid'],
                                                       auth_obj_grp=save_auth['auth_obj_grp'],
                                                       auth_type=save_auth['auth_type'],
                                                       role=save_auth['role'],
                                                       del_ind=False,
                                                       client=client).exists()):

                    if (Authorization.objects.filter(role=save_auth['role']).exists()):
                        Authorization.objects.filter(role=save_auth['role']).update(
                            auth_obj_grp=save_auth['auth_obj_grp'],
                            auth_type=save_auth['auth_type'],
                            role=UserRoles.objects.get(role=save_auth['role']),
                            authorization_created_at=created_time_val,
                            authorization_created_by=created_by_val,
                            authorization_changed_at=changed_at_val,
                            authorization_changed_by=changed_by_val,
                            del_ind=False,
                            client=client)

                    else:
                        save_auth['auth_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_auth['auth_guid'] == 'GUID':
                    obj, created = Authorization.objects.get_or_create(
                        auth_guid=guid_generator(),
                        auth_obj_grp=save_auth['auth_obj_grp'],
                        auth_type=save_auth['auth_type'],
                        role=UserRoles.objects.get(role=save_auth['role']),
                        authorization_created_at=created_time_val,
                        authorization_created_by=created_by_val,
                        authorization_changed_at=changed_at_val,
                        authorization_changed_by=changed_by_val,
                        del_ind=False,
                        client=client)

        Upload_response = list(
            Authorization.objects.filter(del_ind=False).values('auth_guid', 'auth_obj_grp', 'auth_type',
                                                               'role'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_custprodcat':

        Success_message = MSG037

        cust_prod_cat_not_exist: object = UnspscCategoriesCust.objects. \
            filter(del_ind=False).exclude \
            (prod_cat_guid__in=[custprodcat['prod_cat_guid'] for custprodcat in master_data])

        for set_del_int in cust_prod_cat_not_exist:
            set_del_int.del_ind = True
            set_del_int.save()

        for save_custprodcat in master_data:
            product_category_id = save_custprodcat['prod_cat_id']

            created_at_val = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {

                'prod_cat_gud': save_custprodcat['prod_cat_guid'], 'del_ind': False},
                                                                                  'unspsc_categories_cust_created_at')
            created_by_val = django_query_instance.django_filter_value_list_query(UnspscCategoriesCust, {

                'prod_cat_gud': save_custprodcat['prod_cat_guid'], 'del_ind': False},
                                                                                  'unspsc_categories_cust_created_by')

            if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                changed_at_val = datetime.today().date()
                changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                created_by_val = created_by_val[0]
            else:
                created_time_val = datetime.today().date()
                changed_at_val = None
                changed_by_val = None
                created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
            # Below logic is for existing records changed.

            # Check if there is any change in the record if no then skip the record
            if (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                    prod_cat_id=product_category_id,
                                                    client=client).exists()):
                continue

            elif not (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                          prod_cat_id=product_category_id,
                                                          client=client).exists()):

                if (UnspscCategoriesCust.objects.filter(client=client,
                                                        prod_cat_guid=save_custprodcat['prod_cat_guid'], ).exists()):
                    UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                        client=client).update(
                        prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        unspsc_categories_cust_created_at=created_time_val,
                        unspsc_categories_cust_created_by=created_by_val,
                        unspsc_categories_cust_changed_at=changed_at_val,
                        unspsc_categories_cust_changed_by=changed_by_val
                    )

            # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.
            if save_custprodcat['prod_cat_guid'] == '':
                UnspscCategoriesCust.objects.create(
                    prod_cat_guid=guid_generator(),
                    prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                    del_ind=False,
                    client=OrgClients.objects.get(client=client),
                    unspsc_categories_cust_created_at=created_time_val,
                    unspsc_categories_cust_created_by=created_by_val,
                    unspsc_categories_cust_changed_at=changed_at_val,
                    unspsc_categories_cust_changed_by=changed_by_val
                )

        return True, Success_message

    if Table == 'upload_custprodcatdesc':

        for save_custprodcatdesc in master_data:
            if save_custprodcatdesc['del_ind']:

                UnspscCategoriesCustDesc.objects.filter(
                    prod_cat_desc_guid=save_custprodcatdesc['prod_cat_desc_guid']).update(
                    del_ind=True)
            else:

                prod_cat_desc_guid = save_custprodcatdesc['prod_cat_desc_guid']

                if prod_cat_desc_guid == '':
                    prod_cat_desc_guid = guid_generator()

                created_at_val = django_query_instance.django_filter_value_list_query(UnspscCategoriesCustDesc, {
                    'prod_cat_desc_guid': save_custprodcatdesc['prod_cat_desc_guid'], 'del_ind': False},
                                                                                      'unspsc_categories_cust_desc_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(UnspscCategoriesCustDesc, {
                    'prod_cat_desc_guid': save_custprodcatdesc['prod_cat_desc_guid'], 'del_ind': False},
                                                                                      'unspsc_categories_cust_desc_created_by')

                log_values = update_log_info(created_at_val, created_by_val)

                UnspscCategoriesCustDesc.objects.update_or_create(prod_cat_desc_guid=prod_cat_desc_guid,
                                                                  defaults={'prod_cat_desc_guid': prod_cat_desc_guid,
                                                                            'prod_cat_id': UnspscCategories.objects
                                                                  .get(prod_cat_id=save_custprodcatdesc['prod_cat_id'])
                                                                      ,
                                                                            'category_desc':
                                                                                save_custprodcatdesc[
                                                                                    'description'],
                                                                            'language_id': Languages.objects.get(
                                                                                language_id=
                                                                                save_custprodcatdesc['language_id']),
                                                                            'del_ind': False,
                                                                            'unspsc_categories_cust_desc_created_by':
                                                                                log_values[
                                                                                    'created_by_val'],
                                                                            'unspsc_categories_cust_desc_changed_by':
                                                                                log_values[
                                                                                    'changed_by_val'],
                                                                            'client': client
                                                                            })

        Upload_response = list(
            UnspscCategoriesCustDesc.objects.filter(del_ind=False, client=client).values('prod_cat_desc_guid',
                                                                                         'prod_cat_id', 'category_desc',
                                                                                         'language_id'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_detgl':

        for save_detgl in master_data:

            if save_detgl['del_ind']:

                DetermineGLAccount.objects.filter(det_gl_acc_guid=save_detgl['det_gl_acc_guid']).update(
                    del_ind=True)
            else:

                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (DetermineGLAccount.objects.filter(det_gl_acc_guid=save_detgl['det_gl_acc_guid'],
                                                      prod_cat_id=save_detgl['prod_cat_id'],
                                                      item_from_value=save_detgl['from_value'],
                                                      item_to_value=save_detgl['to_value'],
                                                      gl_account=save_detgl['gl_account'],
                                                      gl_acc_default=save_detgl['gl_acc_default'],
                                                      company_id=save_detgl['company_id'],
                                                      del_ind=save_detgl['del_ind'],
                                                      account_assign_cat=save_detgl['account_assign_cat'],
                                                      currency_id=save_detgl['currency_id'],
                                                      client=client).exists()):
                    continue

                elif not (DetermineGLAccount.objects.filter(det_gl_acc_guid=save_detgl['det_gl_acc_guid'],
                                                            prod_cat_id=save_detgl['prod_cat_id'],
                                                            item_from_value=save_detgl['from_value'],
                                                            item_to_value=save_detgl['to_value'],
                                                            gl_account=save_detgl['gl_acc_num'],
                                                            gl_acc_default=save_detgl['gl_acc_default'],
                                                            company_id=save_detgl['company_id'],
                                                            del_ind=save_detgl['del_ind'],
                                                            account_assign_cat=save_detgl['account_assign_cat'],
                                                            currency_id=save_detgl['currency_id'],
                                                            client=client).exists()):

                    if (DetermineGLAccount.objects.filter(
                            gl_acc_num=save_detgl['gl_account'],
                            company_id=save_detgl['company_id'],
                            account_assign_cat=save_detgl['account_assign_cat'],
                            client=client).exists()):

                        DetermineGLAccount.objects.filter(account_assign_value=save_detgl['account_assign_value'],
                                                          account_assign_cat=save_detgl['account_assign_cat'],
                                                          language_id=save_detgl['language_id'],
                                                          company_id=save_detgl['company_id'],
                                                          client=client).update(
                            prod_cat_id=save_detgl['prod_cat_id'],
                            from_value=save_detgl['from_value'],
                            to_value=save_detgl['to_value'],
                            gl_acc_num=save_detgl['gl_account'],
                            gl_acc_default=save_detgl['gl_acc_default'],
                            company_id=save_detgl['company_id'],
                            del_ind=False,
                            account_assign_cat=AccountAssignmentCategory.objects.get
                            (account_assign_cat=save_detgl['account_assign_cat']),
                            currency_id=Currency.objects.get(currency_id=save_detgl['currency_id']),
                            client=OrgClients.objects.get(client=client),

                        )

                    else:
                        save_detgl['det_gl_acc_guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_detgl['det_gl_acc_guid'] == 'GUID':
                    obj, created = DetermineGLAccount.objects.get_or_create(
                        det_gl_acc_guid=guid_generator(),
                        prod_cat_id=save_detgl['prod_cat_id'],
                        from_value=save_detgl['from_value'],
                        to_value=save_detgl['to_value'],
                        gl_acc_num=save_detgl['gl_account'],
                        gl_acc_default=save_detgl['gl_acc_default'],
                        company_id=save_detgl['company_id'],
                        del_ind=False,
                        account_assign_cat=AccountAssignmentCategory.objects.get(
                            account_assign_cat=save_detgl['account_assign_cat']),
                        currency_id=Currency.objects.get(currency_id=save_detgl['currency_id']),
                        client=OrgClients.objects.get(client=client),

                    )
        upload_data_accounting_desc = list(
            DetermineGLAccount.objects.filter(del_ind=False).values('det_gl_acc_guid', 'prod_cat_id', 'from_value'
                                                                    , 'to_value', 'gl_acc_num', 'gl_acc_default'
                                                                    , 'company_id', 'account_assign_cat',
                                                                    'currency_id'))

        return upload_data_accounting_desc, MSG112, MSG113

    if Table == 'Incoterms':

        for save_inco in master_data:
            if save_inco['del_ind']:
                Incoterms.objects.filter(incoterm_key=save_inco['incoterm_key']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Incoterms, {
                    'incoterm_key': save_inco['incoterm_key'], 'del_ind': False}, 'incoterms_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(Incoterms, {
                    'incoterm_key': save_inco['incoterm_key'], 'del_ind': False}, 'incoterms_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()

                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                if not (Incoterms.objects.filter(incoterm_key=save_inco['incoterm_key'],
                                                 description=save_inco['description'],
                                                 del_ind=False).exists()):
                    obj, created = Incoterms.objects.update_or_create(
                        incoterm_key=save_inco['incoterm_key'],
                        defaults={'incoterm_key': save_inco['incoterm_key'],
                                  'description': save_inco['description'],
                                  'incoterms_created_at': created_time_val,
                                  'incoterms_created_by': created_by_val,
                                  'incoterms_changed_at': changed_at_val,
                                  'incoterms_changed_by': changed_by_val,
                                  'del_ind': False
                                  },
                    )

        Upload_response = list(
            Incoterms.objects.filter(del_ind=False).values('incoterm_key', 'description'))

        return Upload_response, MSG112, MSG113

    if Table == 'Payterms':

        for save_payterms in master_data:
            if save_payterms['del_ind']:
                Payterms.objects.filter(payment_term_guid=save_payterms['payment_term_guid'],
                                        payment_term_key=save_payterms['payment_term_key']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Payterms, {
                    'payment_term_guid': save_payterms['payment_term_guid'], 'del_ind': False}, 'payterms_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(Payterms, {
                    'payment_term_guid': save_payterms['payment_term_guid'], 'del_ind': False}, 'payterms_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                payment_term_guid = save_payterms['payment_term_guid']

                if payment_term_guid == '':
                    payment_term_guid = guid_generator()

                Payterms.objects.update_or_create(payment_term_guid=payment_term_guid, defaults={
                    'payment_term_guid': payment_term_guid,
                    'payment_term_key': save_payterms['payment_term_key'],
                    'payterms_created_at': created_time_val,
                    'payterms_created_by': created_by_val,
                    'payterms_changed_at': changed_at_val,
                    'payterms_changed_by': changed_by_val,
                    'del_ind': False,
                    'client': OrgClients.objects.get(client=client)
                }, )

        Upload_response = list(
            Payterms.objects.filter(del_ind=False).values('payment_term_guid', 'payment_term_key'))

        return Upload_response, MSG112, MSG113

    if Table == 'Payterms_desc':

        for save_payterms in master_data:
            if save_payterms['del_ind']:
                Payterms_desc.objects.filter(payment_term_guid=save_payterms['payment_term_guid'],
                                             payment_term_key=save_payterms['payment_term_key']).update(del_ind=True)

            else:
                created_at_val = django_query_instance.django_filter_value_list_query(Payterms_desc, {
                    'payment_term_guid': save_payterms['payment_term_guid'], 'del_ind': False},
                                                                                      'payterms_desc_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(Payterms_desc, {
                    'payment_term_guid': save_payterms['payment_term_guid'], 'del_ind': False},
                                                                                      'payterms_desc_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                payment_term_guid = save_payterms['payment_term_guid']

                if payment_term_guid == '':
                    payment_term_guid = guid_generator()

                Payterms_desc.objects.update_or_create(payment_term_guid=payment_term_guid,
                                                       defaults={'payment_term_guid': payment_term_guid,
                                                                 'payment_term_key': save_payterms['payment_term_key'],
                                                                 'day_limit': save_payterms['day_limit'],
                                                                 'description': save_payterms['description'],
                                                                 'language_id': Languages.objects.get(
                                                                     language_id=save_payterms['language_id']),
                                                                 'payterms_desc_created_at': created_time_val,
                                                                 'payterms_desc_created_by': created_by_val,
                                                                 'payterms_desc_changed_at': changed_at_val,
                                                                 'payterms_desc_changed_by': changed_by_val,
                                                                 'del_ind': False,
                                                                 'client': OrgClients.objects.get(client=client)
                                                                 }, )

        Upload_response = list(
            Payterms_desc.objects.filter(del_ind=False).values('payment_term_guid', 'payment_term_key', 'day_limit',
                                                               'description', 'language_id'))

        return Upload_response, MSG112, MSG113

    if Table == 'OrgAddressMap':
        for save_address_type in master_data:
            if save_address_type['del_ind']:
                OrgAddressMap.objects.filter(address_guid=save_address_type['address_guid'],
                                             address_type=save_address_type['address_type'],
                                             address_number=save_address_type['address_number']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(OrgAddressMap, {
                    'address_guid': save_address_type['address_guid'], 'del_ind': False},
                                                                                      'org_address_map_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(OrgAddressMap, {
                    'address_guid': save_address_type['address_guid'], 'del_ind': False},
                                                                                      'org_address_map_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                address_guid = save_address_type['address_guid']

                if address_guid == '':
                    address_guid = guid_generator()

                OrgAddressMap.objects.update_or_create(address_guid=address_guid, defaults={
                    'address_guid': address_guid,
                    'address_type': save_address_type['address_type'],
                    'address_number': save_address_type['address_number'],
                    'org_address_map_created_at': created_time_val,
                    'org_address_map_created_by': created_by_val,
                    'org_address_map_changed_at': changed_at_val,
                    'org_address_map_changed_by': changed_by_val,
                    'del_ind': False,
                    'client': OrgClients.objects.get(client=client)
                }, )

        Upload_response = list(
            OrgAddressMap.objects.filter(del_ind=False).values('address_guid', 'address_type', 'address_number'))

        return Upload_response, MSG112, MSG113

    if Table == 'OrgAddress':
        for save_address in master_data:
            if save_address['del_ind']:
                OrgAddress.objects.filter(address_guid=save_address['address_guid']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(OrgAddress, {
                    'address_guid': save_address['address_guid'], 'del_ind': False},
                                                                                      'org_address_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(OrgAddress, {
                    'address_guid': save_address['address_guid'], 'del_ind': False},
                                                                                      'org_address_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today().date()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today().date()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                address_guid = save_address['address_guid']
                if address_guid == '':
                    address_guid = guid_generator()

                OrgAddress.objects.update_or_create(address_guid=address_guid, defaults={
                    'address_guid': address_guid,
                    'address_number': save_address['address_number'],
                    'title': save_address['title'],
                    'name1': save_address['name1'],
                    'name2': save_address['name2'],
                    'street': save_address['street'],
                    'area': save_address['area'],
                    'landmark': save_address['landmark'],
                    'city': save_address['city'],
                    'postal_code': save_address['postal_code'],
                    'region': save_address['region'],
                    'mobile_number': save_address['mobile_number'],
                    'telephone_number': save_address['telephone_number'],
                    'fax_number': save_address['fax_number'],
                    'email': save_address['email'],
                    'country_code': Country.objects.get(country_code=save_address['country_code']),
                    'language_id': Languages.objects.get(language_id=save_address['language_id']),
                    'time_zone': TimeZone.objects.get(time_zone=save_address['time_zone']),
                    'org_address_created_at': created_time_val,
                    'org_address_created_by': created_by_val,
                    'org_address_changed_at': changed_at_val,
                    'org_address_changed_by': changed_by_val,
                    'del_ind': False,
                    'client': OrgClients.objects.get(client=client)
                }, )

        Upload_response = list(
            OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                            'street', 'area', 'landmark', 'city', 'postal_code',
                                                            'region',
                                                            'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                            'country_code', 'language_id', 'time_zone'))

        return Upload_response, MSG112, MSG113

    if Table == 'SupplierMaster':
        for save_supp_master in master_data:
            supp_guid = save_supp_master['supp_guid']

            if supp_guid == '':
                supp_guid = guid_generator()

            SupplierMaster.objects.update_or_create(supp_guid=supp_guid, defaults={'supp_guid': supp_guid,
                                                                                   'supplier_id': save_supp_master[
                                                                                       'supplier_id'],
                                                                                   'supp_type': save_supp_master[
                                                                                       'supp_type'],
                                                                                   'name1': save_supp_master['name1'],
                                                                                   'name2': save_supp_master['name2'],
                                                                                   'city': save_supp_master['city'],
                                                                                   'postal_code': save_supp_master[
                                                                                       'postal_code'],
                                                                                   'street': save_supp_master['street'],
                                                                                   'landline': save_supp_master[
                                                                                       'landline'],
                                                                                   'mobile_num': save_supp_master[
                                                                                       'mobile_num'],
                                                                                   'fax': save_supp_master['fax'],
                                                                                   'email': save_supp_master['email'],
                                                                                   'email1': save_supp_master['email1'],
                                                                                   'email2': save_supp_master['email2'],
                                                                                   'email3': save_supp_master['email3'],
                                                                                   'email4': save_supp_master['email4'],
                                                                                   'email5': save_supp_master['email5'],
                                                                                   'output_medium': save_supp_master[
                                                                                       'output_medium'],
                                                                                   'search_term1': save_supp_master[
                                                                                       'search_term1'],
                                                                                   'search_term2': save_supp_master[
                                                                                       'search_term2'],
                                                                                   'duns_number': save_supp_master[
                                                                                       'duns_number'],
                                                                                   'block_date': save_supp_master[
                                                                                       'block_date'],
                                                                                   'block': save_supp_master['block'],
                                                                                   'working_days': save_supp_master[
                                                                                       'working_days'],
                                                                                   'is_active': save_supp_master[
                                                                                       'is_active'],
                                                                                   'registration_number':
                                                                                       save_supp_master[
                                                                                           'registration_number'],
                                                                                   'country_code': Country.objects.get(
                                                                                       country_code='IN'),
                                                                                   'currency_id': Currency.objects.get(
                                                                                       currency_id='INR'),
                                                                                   'language_id': Languages.objects.get(
                                                                                       language_id='EN'),
                                                                                   'del_ind': False,
                                                                                   'client': OrgClients.objects.get(
                                                                                       client=client)
                                                                                   }, )

        Upload_response = list(
            SupplierMaster.objects.filter(del_ind=False).values('supplier_id', 'supp_type', 'name1', 'name2', 'city',
                                                                'postal_code', 'street', 'landline', 'mobile_num',
                                                                'fax',
                                                                'email', 'email1', 'email2', 'email3', 'email4',
                                                                'email5',
                                                                'output_medium', 'search_term1', 'search_term2',
                                                                'duns_number', 'block_date', 'block', 'working_days',
                                                                'is_active', 'registration_number', 'del_ind',
                                                                'client_id',
                                                                'country_code', 'currency_id', 'language_id'))

        return Upload_response, MSG112, MSG113


def save_product_cat_cust_desc_data_into_db(prodcatdesc_data):
    prodcatdesc_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if prodcatdesc_data['action'] == CONST_ACTION_DELETE:
        for prodcatdesc_detail in prodcatdesc_data['data']:
            django_query_instance.django_update_query(UnspscCategoriesCustDesc,
                                                      {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                       'language_id': prodcatdesc_detail['language_id']},
                                                      {'del_ind': True,
                                                       'unspsc_categories_cust_desc_changed_at': datetime.today(),
                                                       'unspsc_categories_cust_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for prodcatdesc_detail in prodcatdesc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnspscCategoriesCustDesc,
                                                                {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                                 'language_id': prodcatdesc_detail['language_id']
                                                                 }):
                guid = guid_generator()
                prodcatdesc_db_dictionary = {'prod_cat_desc_guid': guid,
                                             'prod_cat_id': UnspscCategories.objects.get(
                                                 prod_cat_id=prodcatdesc_detail['prod_cat_id']),
                                             'category_desc': prodcatdesc_detail['description'],
                                             'language_id': Languages.objects.get(
                                                 language_id=prodcatdesc_detail['language_id']),
                                             'unspsc_categories_cust_desc_created_at': datetime.today(),
                                             'unspsc_categories_cust_desc_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'unspsc_categories_cust_desc_changed_at': datetime.today(),
                                             'unspsc_categories_cust_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'client': client
                                             }

                prodcatdesc_db_list.append(prodcatdesc_db_dictionary)
            else:
                django_query_instance.django_update_query(UnspscCategoriesCustDesc,
                                                          {'prod_cat_id': prodcatdesc_detail['prod_cat_id'],
                                                           'language_id': prodcatdesc_detail['language_id'],
                                                           'prod_cat_desc_guid':prodcatdesc_detail ['prod_cat_desc_guid']},
                                                          {'category_desc': prodcatdesc_detail['description'],
                                                           'prod_cat_id': UnspscCategories.objects.get(
                                                               prod_cat_id=prodcatdesc_detail['prod_cat_id']),
                                                           'language_id': Languages.objects.get(
                                                               language_id=prodcatdesc_detail['language_id']),
                                                           'unspsc_categories_cust_desc_changed_at': datetime.today(),
                                                           'unspsc_categories_cust_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': prodcatdesc_detail['del_ind'],
                                                           'client': OrgClients.objects.get(client=client)})
        bulk_create_entry_db(UnspscCategoriesCustDesc, prodcatdesc_db_list)
        message = MSG112
    upload_response = get_configuration_data(UnspscCategoriesCustDesc, {'del_ind': False},
                                             ['prod_cat_desc_guid', 'prod_cat_id', 'category_desc', 'language_id'])

    return upload_response, message


def save_work_flow_schema_data_into_db(workflowschema_data):
    workflowschema_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    wrksch_type_field = ''
    client = global_variables.GLOBAL_CLIENT
    if workflowschema_data['action'] == CONST_ACTION_DELETE:
        for workflowschema_detail in workflowschema_data['data']:
            django_query_instance.django_update_query(WorkflowSchema,
                                                      {'workflow_schema': workflowschema_detail['workflow_schema'],
                                                                 'company_id': workflowschema_detail['company_id']},
                                                      {'del_ind': True,
                                                       'workflow_schema_changed_at': datetime.today(),
                                                       'workflow_schema_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for workflowschema_detail in workflowschema_data['data']:
            wrksch_type_field = workflowschema_detail['workflow_schema']
            # if entry is not exists in db

            if not django_query_instance.django_existence_check(WorkflowSchema,
                                                                {'workflow_schema': workflowschema_detail['workflow_schema'],
                                                                 'company_id': workflowschema_detail['company_id']
                                                                 }):
                guid = guid_generator()
                workflowschema_db_dictionary = {'workflow_schema_guid': guid,
                                                'workflow_schema': workflowschema_detail['workflow_schema'],
                                                'app_types': ApproverType.objects.get(
                                                    app_types=workflowschema_detail['app_types']),
                                                'company_id': workflowschema_detail['company_id'],
                                                'workflow_schema_created_at': datetime.today(),
                                                'workflow_schema_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                'workflow_schema_changed_at': datetime.today(),
                                                'workflow_schema_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                'client': OrgClients.objects.get(client=client)}
                workflowschema_db_list.append(workflowschema_db_dictionary)
            else:
                django_query_instance.django_update_query(WorkflowSchema,
                                                          {'workflow_schema': workflowschema_detail[
                                                              'workflow_schema'],
                                                           'workflow_schema_guid':workflowschema_detail['workflow_schema_guid']},
                                                          {'workflow_schema': workflowschema_detail['workflow_schema'],
                                                           'app_types': ApproverType.objects.get(
                                                               app_types=workflowschema_detail['app_types']),
                                                           'company_id': workflowschema_detail['company_id'],
                                                           'workflow_schema_changed_at': datetime.today(),
                                                           'workflow_schema_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': OrgClients.objects.get(client=client),
                                                           'del_ind': workflowschema_detail['del_ind']})
        bulk_create_entry_db(WorkflowSchema, workflowschema_db_list)
        fieldtypedesc_instance.update_usedFlag(wrksch_type_field)
        message = MSG112
    upload_response = get_configuration_data(WorkflowSchema, {'del_ind': False},
                                             ['workflow_schema_guid', 'workflow_schema', 'company_id', 'app_types'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'workflow_schema'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_spend_limit_data_into_db(spendlimit_data):
    spendlimit_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if spendlimit_data['action'] == CONST_ACTION_DELETE:
        for spendlimit_detail in spendlimit_data['data']:
            django_query_instance.django_update_query(SpendLimitId,
                                                      {'spender_username': spendlimit_detail['spender_username'],
                                                       'company_id': spendlimit_detail['company_id']},
                                                      {'del_ind': True,
                                                       'spend_limit_id_changed_at': datetime.today(),
                                                       'spend_limit_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:

        for spendlimit_detail in spendlimit_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(SpendLimitId,
                                                                {'spender_username': spendlimit_detail[
                                                                    'spender_username'],
                                                                 'company_id': spendlimit_detail['company_id'],
                                                                 'spend_guid':spendlimit_detail ['spend_guid']}):
                guid = guid_generator()
                spendlimit_db_dictionary = {'spend_guid': guid,
                                            'spend_code_id': spendlimit_detail['spend_code_id'],
                                            'spender_username': spendlimit_detail['spender_username'],
                                            'company_id': spendlimit_detail['company_id'],
                                            'spend_limit_id_created_at': datetime.today(),
                                            'spend_limit_id_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                            'spend_limit_id_changed_at': datetime.today(),
                                            'spend_limit_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                            'client': OrgClients.objects.get(client=client),
                                            }
                spendlimit_db_list.append(spendlimit_db_dictionary)
            else:
                django_query_instance.django_update_query(SpendLimitId,
                                                          {'spender_username': spendlimit_detail[
                                                              'spender_username'],
                                                           'company_id': spendlimit_detail['company_id'],
                                                           'spend_guid':spendlimit_detail ['spend_guid']},
                                                          {'spend_code_id': spendlimit_detail['spend_code_id'],
                                                           'spender_username': spendlimit_detail['spender_username'],
                                                           'company_id': spendlimit_detail['company_id'],
                                                           'spend_limit_id_changed_at': datetime.today(),
                                                           'spend_limit_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': OrgClients.objects.get(client=client),
                                                           'del_ind': spendlimit_detail['del_ind']})
        bulk_create_entry_db(SpendLimitId, spendlimit_db_list)
        message = MSG112
    upload_response = get_configuration_data(SpendLimitId, {'del_ind': False},
                                             ['spend_guid', 'spend_code_id', 'spender_username', 'company_id'])

    return upload_response, message


def save_address_type_data_into_db(addresstype_data):
    addresstype_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    address_type_field = ''
    client = global_variables.GLOBAL_CLIENT
    if addresstype_data['action'] == CONST_ACTION_DELETE:
        for addresstype_detail in addresstype_data['data']:
            django_query_instance.django_update_query(OrgAddressMap,
                                                      {'address_guid': addresstype_detail[
                                                          'address_guid']},
                                                      {'del_ind': True,
                                                       'org_address_map_created_at': datetime.today(),
                                                       'org_address_map_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:

        for addresstype_detail in addresstype_data['data']:
            address_type_field = addresstype_detail['address_type']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgAddressMap,
                                                                {'address_guid': addresstype_detail[
                                                                    'address_guid']}):
                guid = guid_generator()
                addresstype_db_dictionary = {'address_guid': guid,
                                             'address_number': addresstype_detail['address_number'],
                                             'address_type': addresstype_detail['address_type'],
                                             'company_id': addresstype_detail['company_id'],
                                             'org_address_map_created_at': datetime.today(),
                                             'org_address_map_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'org_address_map_changed_at': datetime.today(),
                                             'org_address_map_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'client': OrgClients.objects.get(client=client),
                                             }
                addresstype_db_list.append(addresstype_db_dictionary)
            else:
                django_query_instance.django_update_query(OrgAddressMap,
                                                          {'address_guid': addresstype_detail[
                                                              'address_guid']},
                                                          {'address_guid': addresstype_detail[
                                                              'address_guid'],
                                                           'address_number': addresstype_detail['address_number'],
                                                           'address_type': addresstype_detail['address_type'],
                                                           'company_id': addresstype_detail['company_id'],
                                                           'org_address_map_changed_at': datetime.today(),
                                                           'org_address_map_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': OrgClients.objects.get(client=client),
                                                           'del_ind': addresstype_detail['del_ind']})
        bulk_create_entry_db(OrgAddressMap, addresstype_db_list)
        fieldtypedesc_instance.update_usedFlag(address_type_field)

        message = MSG112
    upload_response = get_configuration_data(OrgAddressMap, {'del_ind': False},
                                             ['address_guid', 'address_number', 'address_type', 'company_id'])

    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'address_type'},
                                                                             ['field_type_id', 'field_type_desc'])
    return upload_response, message, upload_fieldtypedesc


def save_glaccount_data_into_db(glaccount_data):
    glaccount_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if glaccount_data['action'] == CONST_ACTION_DELETE:
        for glaccount_detail in glaccount_data['data']:
            django_query_instance.django_update_query(DetermineGLAccount,
                                                      {'det_gl_acc_guid': glaccount_detail[
                                                          'det_gl_acc_guid']},
                                                      {'del_ind': True,
                                                       'determine_gl_account_created_at': datetime.today(),
                                                       'determine_gl_account_created_by': global_variables.GLOBAL_LOGIN_USERNAME})

        message = MSG113
    else:

        for glaccount_detail in glaccount_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(DetermineGLAccount,
                                                                {'det_gl_acc_guid': glaccount_detail[
                                                                    'det_gl_acc_guid']}):
                guid = guid_generator()
                glaccount_db_dictionary = {'det_gl_acc_guid': guid,
                                           'prod_cat_id': glaccount_detail['prod_cat_id'],
                                           'gl_acc_num': glaccount_detail['gl_account'],
                                           'gl_acc_default': glaccount_detail['gl_acc_default'],
                                           'account_assign_cat': AccountAssignmentCategory.objects.
                                               get(account_assign_cat=glaccount_detail['account_assign_cat']),
                                           'company_id': glaccount_detail['company_id'],
                                           'item_from_value': glaccount_detail['from_value'],
                                           'item_to_value': glaccount_detail['to_value'],
                                           'currency_id': Currency.objects.
                                               get(currency_id=glaccount_detail['currency_id']),
                                           'determine_gl_account_created_at': datetime.today(),
                                           'determine_gl_account_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'determine_gl_account_changed_at': datetime.today(),
                                           'determine_gl_account_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'client': OrgClients.objects.get(client=client),
                                           }
                glaccount_db_list.append(glaccount_db_dictionary)
            else:
                django_query_instance.django_update_query(DetermineGLAccount,
                                                          {'det_gl_acc_guid': glaccount_detail[
                                                              'det_gl_acc_guid']},
                                                          {'det_gl_acc_guid': glaccount_detail[
                                                              'det_gl_acc_guid'],
                                                           'prod_cat_id': glaccount_detail['prod_cat_id'],
                                                           'gl_acc_num': glaccount_detail['gl_account'],
                                                           'gl_acc_default': glaccount_detail['gl_acc_default'],
                                                           'account_assign_cat': AccountAssignmentCategory.objects.
                                                          get(account_assign_cat=glaccount_detail[
                                                               'account_assign_cat']),
                                                           'company_id': glaccount_detail['company_id'],
                                                           'item_from_value': glaccount_detail['from_value'],
                                                           'item_to_value': glaccount_detail['to_value'],
                                                           'currency_id': Currency.objects.
                                                          get(currency_id=glaccount_detail['currency_id']),
                                                           'determine_gl_account_changed_at': datetime.today(),
                                                           'determine_gl_account_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': OrgClients.objects.get(client=client),
                                                           'del_ind': glaccount_detail['del_ind']})
        bulk_create_entry_db(DetermineGLAccount, glaccount_db_list)
        message = MSG112
    upload_response = get_configuration_data(DetermineGLAccount, {'del_ind': False},

                                             ['det_gl_acc_guid', 'prod_cat_id', 'gl_acc_num',
                                              'gl_acc_default', 'account_assign_cat', 'company_id',
                                              'item_from_value','item_to_value', 'currency_id'])


    return upload_response, message


def save_prod_cat_image_to_db(prod_cat, file_name, attached_file):
    """

    :param prod_cat:
    :param file_name:
    :param attached_file:
    :return:
    """
    image_type = get_image_type(CONST_UNSPSC_IMAGE_TYPE)
    if django_query_instance.django_existence_check(ImagesUpload,
                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                     'image_id': prod_cat}):
        django_query_instance.django_get_query(ImagesUpload,
                                               {'client': global_variables.GLOBAL_CLIENT,
                                                'image_id': prod_cat}).image_url.delete(save=True)
        django_query_instance.django_filter_delete_query(ImagesUpload,
                                                         {'client': global_variables.GLOBAL_CLIENT,
                                                          'image_id': prod_cat})
    django_query_instance.django_create_query(ImagesUpload, {
        'images_upload_guid': guid_generator(),
        'client': global_variables.GLOBAL_CLIENT,
        'image_id': prod_cat,
        'image_url': attached_file['prod_cat_image'],
        'image_name': file_name,
        'image_default': True,
        'image_type': image_type,
        'created_at': datetime.today(),
        'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
        'del_ind': False
    })


#
def save_company_data_into_db(company_data):
    # orgcompanies_not_exist: object = OrgCompanies.objets.flter(delind=False).exclude \
    #     (company_guid__in=[orgcompanies['company_guid'] for orgcompanies in master_data])
    #
    # for set_del_int in orgcompanies_not_exist:
    #     set_del_int.del_ind = True
    #     set_del_int.save()

    company_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if company_data['action'] == CONST_ACTION_DELETE:
        for company_detail in company_data['data']:
            django_query_instance.django_update_query(OrgCompanies,
                                                      {'company_id': company_detail['company_id']},
                                                      {'del_ind': True,
                                                       'org_companies_changed_at': datetime.today(),
                                                       'org_companies_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for company_detail in company_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgCompanies,
                                                                {'company_id': company_detail['company_id']}):
                guid = guid_generator()
                company_db_dictionary = {'company_guid': guid,
                                         'object_id':company_detail ['object_id'],
                                         'name1': company_detail['name1'],
                                         'name2': company_detail['name2'],
                                         'company_id': company_detail['company_id'],

                                         'del_ind': False,
                                         'client': OrgClients.objects.get(client=client),
                                         'org_companies_changed_at': datetime.today(),
                                         'org_companies_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         'org_companies_created_at': datetime.today(),
                                         'org_companies_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                         }
                company_db_list.append(company_db_dictionary)

            else:

                django_query_instance.django_update_query(OrgCompanies,
                                                          {'company_id': company_detail['company_id']},
                                                          {
                                                              'object_id': company_detail['object_id'],
                                                              'name1': company_detail['name1'],
                                                              'name2': company_detail['name2'],
                                                              'company_id': company_detail['company_id'],
                                                              'org_companies_changed_at': datetime.today(),
                                                              'org_companies_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                              'del_ind': False,
                                                              'client': OrgClients.objects.get(client=client), })
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(OrgCompanies, company_db_list)
        message = MSG112

    upload_response = get_configuration_data(OrgCompanies, {'del_ind': False},
                                             ['object_id','company_guid', 'name1', 'name2', 'company_id'])

    return upload_response, message

def save_product_cat_cust_data_into_db(prodcat_data):
    prodcat_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if prodcat_data['action'] == CONST_ACTION_DELETE:
        for prodcat_detail in prodcat_data['data']:
            django_query_instance.django_update_query(UnspscCategoriesCust,
                                                      {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                       },
                                                      {'del_ind': True,
                                                       'unspsc_categories_cust_changed_at': datetime.today(),
                                                       'unspsc_categories_cust_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for prodcat_detail in prodcat_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(UnspscCategoriesCust,
                                                                {'prod_cat_id': prodcat_detail['prod_cat_id'],

                                                                 }):
                guid = guid_generator()
                prodcat_db_dictionary = {'prod_cat_guid': guid,
                                             'prod_cat_id': UnspscCategories.objects.get(
                                                 prod_cat_id=prodcat_detail['prod_cat_id']),
                                             'unspsc_categories_cust_created_at': datetime.today(),
                                             'unspsc_categories_cust_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'unspsc_categories_cust_changed_at': datetime.today(),
                                             'unspsc_categories_cust_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                             'client': client
                                             }

                prodcat_db_list.append(prodcat_db_dictionary)
            else:
                django_query_instance.django_update_query(UnspscCategoriesCust,
                                                          {'prod_cat_id': prodcat_detail['prod_cat_id'],
                                                           'prod_cat_guid': prodcat_detail[
                                                               'prod_cat_guid']},
                                                          {'prod_cat_id': UnspscCategories.objects.get(
                                                               prod_cat_id=prodcat_detail['prod_cat_id']),
                                                           'unspsc_categories_cust_changed_at': datetime.today(),
                                                           'unspsc_categories_cust_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': prodcat_detail['del_ind'],
                                                           'client': OrgClients.objects.get(client=client)})
        bulk_create_entry_db(UnspscCategoriesCust,prodcat_db_list)
        message = MSG112
    upload_response = get_configuration_data(UnspscCategoriesCust, {'del_ind': False},
                                             ['prod_cat_guid', 'prod_cat_id'])

    return upload_response, message

def save_auth_data_into_db(auth_data):
    auth_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    auth_type_field = ''
    client = global_variables.GLOBAL_CLIENT
    if auth_data['action'] == CONST_ACTION_DELETE:
        for auth_detail in auth_data['data']:
            auth_type_field = auth_detail['auth_obj_grp']
            django_query_instance.django_update_query(Authorization,
                                                      {'auth_obj_grp': auth_detail['auth_obj_grp']},
                                                      {'del_ind': True,
                                                       'authorization_changed_at': datetime.today(),
                                                       'authorization_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
            fieldtypedesc_instance.reset_usedFlag(auth_type_field)
        message = MSG113
    else:
        for auth_detail in auth_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(Authorization,
                                                                {'auth_obj_grp': auth_detail
                                                                ['auth_obj_grp']}):
                guid = guid_generator()
                auth_db_dictionary = {'auth_guid': guid,
                                      'auth_obj_grp': auth_detail['auth_obj_grp'],
                                      'auth_type': auth_detail['auth_type'],
                                      'role': UserRoles.objects.get(role=auth_detail['role']),
                                      'del_ind': False,
                                      'client': client,
                                      'authorization_changed_at': datetime.today(),
                                      'authorization_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                      'authorization_created_at': datetime.today(),
                                      'authorization_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                      }
                auth_db_list.append(auth_db_dictionary)

            else:

                django_query_instance.django_update_query(Authorization,
                                                          {'auth_obj_grp': auth_detail['auth_obj_grp']},
                                                          {
                                                              'auth_obj_grp': auth_detail['auth_obj_grp'],
                                                              'auth_type': auth_detail['auth_type'],
                                                              'role': UserRoles.objects.get(role=auth_detail['role']),
                                                              'authorization_changed_at': datetime.today(),
                                                              'authorization_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                              'client': client,
                                                              'del_ind': False})
        # guid = number_range_data['account_assign_guid']
        # if guid == '':
        # guid = guid_generator()
        bulk_create_entry_db(Authorization, auth_db_list)
        fieldtypedesc_instance.update_usedFlag(auth_type_field)
        message = MSG112
    upload_response = get_configuration_data(Authorization, {'del_ind': False},
                                             ['auth_guid', 'auth_obj_grp', 'auth_type', 'role',
                                              ])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'auth_obj_grp'},
                                                                             ['field_type_id', 'field_type_desc'])
    return upload_response, message,upload_fieldtypedesc

