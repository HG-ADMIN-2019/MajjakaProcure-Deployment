from datetime import datetime
import datetime

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.functions.camel_case import convert_to_camel_case
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.constants.constants import CONST_ACTION_DELETE, CONST_SC_TRANS_TYPE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries, bulk_create_entry_db
from eProc_Basic.Utilities.functions.range_check import range_check
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data, FieldTypeDescription
from eProc_Configuration.models import NumberRanges, \
    Country, CalenderHolidays, Incoterms, \
    SystemSettingsConfig, CalenderConfig, Languages
from eProc_Configuration.models.development_data import *
from eProc_Configuration.models.development_data import OrgClients
from eProc_Configuration.models.development_data import DocumentType
from eProc_Basic.Utilities.messages.messages import MSG112, MSG113
from eProc_Basic.Utilities.functions.guid_generator import guid_generator, random_int
from eProc_Configuration.models.development_data import MessagesId
from eProc_Basic.Utilities.functions.log_function import update_log_info
from eProc_Org_Model.Utilities import client

django_query_instance = DjangoQueries()


def save_client_data_into_db(client_data):
    """

    """
    client_db_list = []
    if client_data['action'] == CONST_ACTION_DELETE:
        for client_detail in client_data['data']:
            django_query_instance.django_update_query(OrgClients,
                                                      {'client': client_detail['client']},
                                                      {'del_ind': True,
                                                       'org_clients_changed_at': datetime.datetime.now(),
                                                       'org_clients_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                      )
        message = MSG113
    else:
        for client_detail in client_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(OrgClients,
                                                                {'client': client_detail['client']}):
                client_db_dictionary = {'client': client_detail['client'],
                                        'description':convert_to_camel_case( client_detail['description']),
                                        'org_clients_created_at': datetime.datetime.now(),
                                        'org_clients_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                        }
                client_db_list.append(client_db_dictionary)
            else:
                django_query_instance.django_update_query(OrgClients,
                                                          {'client': client_detail['client']},
                                                          {'client': client_detail['client'],
                                                           'description':convert_to_camel_case( client_detail['description']),
                                                           'org_clients_changed_at': datetime.datetime.now(),
                                                           'org_clients_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})
        bulk_create_entry_db(OrgClients, client_db_list)
        message = MSG112
    upload_response = get_configuration_data(OrgClients, {'del_ind': False}, ['client', 'description'])

    return upload_response, message


def save_number_range_data_into_db(number_range_data):
    """

    """
    number_range_db_list = []
    range_check_flag = False
    client = global_variables.GLOBAL_CLIENT
    abc = range_check(6,3,6)
    doc_type = ''
    if number_range_data['action'] == CONST_ACTION_DELETE:
        for number_range_detail in number_range_data['data']:
            doc_type = number_range_detail['document_type']
            if not django_query_instance.django_existence_check(TransactionTypes,
                                                                {'sequence': number_range_detail['sequence'],
                                                                 'document_type': number_range_detail['document_type'],
                                                                 'client': client}):
                django_query_instance.django_update_query(NumberRanges,
                                                          {'sequence': number_range_detail['sequence'],
                                                           'document_type': number_range_detail['document_type'],
                                                           'client': client},

                                                          {'del_ind': True,
                                                           'number_ranges_changed_at': datetime.datetime.now(),
                                                           'number_ranges_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                                                          )
        message = MSG113
    else:
        for number_range_detail in number_range_data['data']:
            doc_type = number_range_detail['document_type']
            delete_flag = True
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(NumberRanges,
                                                                {'sequence': number_range_detail['sequence'],
                                                                 'client': client,
                                                                 'document_type': number_range_detail[
                                                                     'document_type'],
                                                                 }):
                number_ranges = django_query_instance.django_filter_query(NumberRanges,
                                                                         {'client': client,
                                                                          'del_ind':False,
                                                                         'document_type': number_range_detail['document_type']},None,None)
                for number_range in number_ranges:
                    range_check_flag = range_check(number_range_detail['starting'],number_range['starting'],number_range['ending'])
                    if range_check_flag:
                        break
                    else:
                        range_check_flag = range_check(number_range_detail['ending'], number_range['starting'],
                                                  number_range['ending'])
                        if range_check_flag:
                            break
                if not range_check_flag:
                    num_guid = guid_generator()
                    number_range_db_dictionary = {'guid': num_guid,
                                                  'sequence': number_range_detail['sequence'],
                                                  'starting': number_range_detail['starting'],
                                                  'ending': number_range_detail['ending'],
                                                  'current': number_range_detail['current'],
                                                  'del_ind': False,
                                                  'client': client,
                                                  'document_type': DocumentType.objects.get
                                                  (document_type=number_range_detail[
                                                      'document_type']),
                                                  'number_ranges_changed_at': datetime.datetime.now(),
                                                  'number_ranges_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                  'number_ranges_created_at': datetime.datetime.now(),
                                                  'number_ranges_created_by': global_variables.GLOBAL_LOGIN_USERNAME, }
                    number_range_db_list.append(number_range_db_dictionary)

            else:
                if number_range_detail['del_ind']:
                    if django_query_instance.django_existence_check(NumberRanges,
                                                                    {'sequence': number_range_detail['sequence'],
                                                                     'client': client,
                                                                     'document_type':
                                                                         number_range_detail[
                                                                             'document_type'],
                                                                     }):
                        delete_flag = False
                if delete_flag:
                    django_query_instance.django_update_query(NumberRanges,
                                                              {'sequence': number_range_detail
                                                              ['sequence'],
                                                               'client': client,
                                                               'document_type': number_range_detail[
                                                                   'document_type'],
                                                               },
                                                              {'sequence': number_range_detail['sequence'],
                                                               'starting': number_range_detail['starting'],
                                                               'ending': number_range_detail['ending'],
                                                               'current': number_range_detail['current'],
                                                               'document_type': DocumentType.objects.get(
                                                                   document_type=number_range_detail['document_type']),

                                                               'number_ranges_changed_at': datetime.datetime.now(),
                                                               'number_ranges_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                               'client': client,
                                                               'del_ind': False})

        bulk_create_entry_db(NumberRanges, number_range_db_list)
        message = MSG112
    upload_response = get_configuration_data(NumberRanges,
                                             {'del_ind': False, 'document_type': doc_type, 'client': client},
                                             ['guid', 'sequence', 'starting', 'ending',
                                              'current', 'document_type',
                                              ])

    return upload_response, message


def save_app_data_into_db(basic_data, Table, client, elseif=None):
    if Table == 'upload_clients':

        for save_client in basic_data:
            if save_client['del_ind']:
                OrgClients.objects.filter(client=save_client['client']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(OrgClients, {
                    'client': save_client['client'], 'del_ind': False}, 'org_clients_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(OrgClients, {
                    'client': save_client['client'], 'del_ind': False}, 'org_clients_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                if not (OrgClients.objects.filter(client=save_client['client'],
                                                  description=save_client['description'], del_ind=False).exists()):
                    obj, created = OrgClients.objects.update_or_create(
                        client=save_client['client'],
                        defaults={'client': save_client['client'],
                                  'description': save_client['description'],
                                  'org_clients_created_at': created_time_val,
                                  'org_clients_created_by': created_by_val,
                                  'org_clients_changed_at': changed_at_val,
                                  'org_clients_changed_by': changed_by_val,
                                  'del_ind': False},
                    )

        Upload_response = list(OrgClients.objects.filter(del_ind=False).values('client', 'description'))

        return Upload_response, MSG112, MSG113

    # if Table == 'CalenderSettings':
    #
    #     for save_calender in basic_data:
    #         if save_calender['del_ind']:
    #             CalenderSettings.objects.filter(calender_id=save_calender['calender_id']).update(del_ind=True)
    #         else:
    #             if not (CalenderSettings.objects.filter(calender_id=save_calender['calender_id'],
    #                                                     description=save_calender['description'],
    #                                                     year=save_calender['year'],
    #                                                     working_days=save_calender['working_days'],
    #                                                     del_ind=False, country_code=save_calender['country']).exists()):
    #                 obj, created = CalenderSettings.objects.update_or_create(
    #                     calender_id=save_calender['calender_id'],
    #                     defaults={'calender_id': save_calender['calender_id'],
    #                               'description': save_calender['description'],
    #                               'year': save_calender['year'],
    #                               'working_days': save_calender['working_days'],
    #                               'del_ind': False, 'client': OrgClients.objects.get(client=client),
    #                               'country_code': Country.objects.get(country_code=save_calender['country'])
    #                               },
    #                 )
    #     Upload_response = list(
    #         CalenderSettings.objects.filter(del_ind=False).values('calender_id', 'description', 'year', 'working_days'))
    #
    #     return Upload_response, MSG112, MSG113

    if Table == 'CalenderConfig':

        for save_calender in basic_data:
            if save_calender['del_ind']:
                if CalenderHolidays.objects.filter(calender_id=save_calender['calender_id']).exists():
                    CalenderHolidays.objects.filter(calender_id=save_calender['calender_id']).update(
                        del_ind=True)
                CalenderConfig.objects.filter(calender_config_guid=save_calender['calendar_config_guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(CalenderConfig, {
                    'calender_config_guid': save_calender['calendar_config_guid'], 'del_ind': False},
                                                                                      'calender_config_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(CalenderConfig, {
                    'calender_id': save_calender['calender_id'], 'del_ind': False}, 'calender_config_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                print(update_log_info(created_at_val, created_by_val))
                calender_config_guid = save_calender['calendar_config_guid']

                if calender_config_guid == '':
                    calender_config_guid = guid_generator()

                CalenderConfig.objects.update_or_create(calender_config_guid=calender_config_guid, defaults={
                    'calender_config_guid': calender_config_guid,
                    'calender_id': save_calender['calender_id'],
                    'description': save_calender['description'],
                    'year': save_calender['year'],
                    'working_days': save_calender['working_days'],
                    'del_ind': False,
                    'country_code': Country.objects.get(country_code=save_calender['country']),
                    'calender_config_created_at': created_time_val,
                    'calender_config_created_by': created_by_val,
                    'calender_config_changed_at': changed_at_val,
                    'calender_config_changed_by': changed_by_val,
                    'client': OrgClients.objects.get(client=client)
                })

        calender_data = django_query_instance.django_filter_query(CalenderConfig,
                                                                  {'del_ind': False},
                                                                  None,
                                                                  ['calender_config_guid', 'calender_id', 'description',
                                                                   'year', 'working_days', 'country_code'])
        country_code = list(CalenderConfig.objects.filter(del_ind=False).values_list('country_code', flat=True))
        country_desc = django_query_instance.django_filter_query(Country,
                                                                 {'country_code__in': country_code,
                                                                  'del_ind': False},
                                                                 None,
                                                                 None)

        for calender in calender_data:
            for country in country_desc:
                if calender['country_code'] == country['country_code']:
                    if country['country_name']:
                        calender['country_desc'] = country['country_name']
                    else:
                        calender['country_desc'] = country['country_code']

        return calender_data, MSG112, MSG113

    if Table == 'CalenderHolidays':

        for save_calender in basic_data:
            if save_calender['del_ind']:
                CalenderHolidays.objects.filter(calender_holiday_guid=save_calender['calender_holiday_guid'],
                                                calender_id=save_calender['calender_id']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(CalenderHolidays, {
                    'calender_holiday_guid': save_calender['calender_holiday_guid'], 'del_ind': False}, 'created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(CalenderHolidays, {
                    'calender_holiday_guid': save_calender['calender_holiday_guid'], 'del_ind': False}, 'created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                calender_holiday_guid = save_calender['calender_holiday_guid']

                if calender_holiday_guid == '':
                    calender_holiday_guid = guid_generator()

                CalenderHolidays.objects.update_or_create(calender_holiday_guid=calender_holiday_guid, defaults={
                    'calender_holiday_guid': calender_holiday_guid,
                    'calender_id': save_calender['calender_id'],
                    'holiday_description': save_calender['holiday_description'],
                    'from_date': save_calender['from_date'],
                    'to_date': save_calender['to_date'],
                    'created_at': created_time_val,
                    'created_by': created_by_val,
                    'changed_at': changed_at_val,
                    'changed_by': changed_by_val,
                    'client': OrgClients.objects.get(client=client)
                },
                                                          )

        Upload_response = list(
            CalenderHolidays.objects.filter(del_ind=False).values('calender_holiday_guid', 'calender_id',
                                                                  'holiday_description', 'from_date',
                                                                  'to_date'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_doctyp':

        for save_doctypes in basic_data:
            if save_doctypes['del_ind']:
                DocumentType.objects.filter(document_type=save_doctypes['document_type']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(DocumentType, {
                    'document_type': save_doctypes['document_type'], 'del_ind': False}, 'document_type_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(DocumentType, {
                    'document_type': save_doctypes['document_type'], 'del_ind': False}, 'document_type_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                if not (DocumentType.objects.filter(document_type=save_doctypes['document_type'],
                                                    document_type_desc=save_doctypes['document_type_desc'],
                                                    del_ind=False).exists()):
                    obj, created = DocumentType.objects.update_or_create(document_type=save_doctypes['document_type'],
                                                                         defaults={'document_type': save_doctypes[
                                                                             'document_type'],
                                                                                   'document_type_desc': save_doctypes[
                                                                                       'document_type_desc'],
                                                                                   'document_type_created_at': created_time_val,
                                                                                   'document_type_created_by': created_by_val,
                                                                                   'document_type_changed_at': changed_at_val,
                                                                                   'document_type_changed_by': changed_by_val,
                                                                                   'del_ind': False}, )

        Upload_response = list(DocumentType.objects.filter(del_ind=False).values('document_type', 'document_type_desc'))
        return Upload_response, MSG112, MSG113

    if Table == 'upload_accasscat':

        for save_accasscats in basic_data:
            if save_accasscats['del_ind']:
                AccountAssignmentCategory.objects.filter \
                    (account_assign_cat=save_accasscats['account_assign_cat']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(AccountAssignmentCategory, {
                    'account_assign_cat': save_accasscats['account_assign_cat'], 'del_ind': False},
                                                                                      'account_assignment_category_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(AccountAssignmentCategory, {
                    'account_assign_cat': save_accasscats['account_assign_cat'], 'del_ind': False},
                                                                                      'account_assignment_category_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

            if not (
                    AccountAssignmentCategory.objects.filter
                        (account_assign_cat=save_accasscats['account_assign_cat'],
                         description=save_accasscats['description'],
                         del_ind=False).exists()):
                obj, created = AccountAssignmentCategory.objects.update_or_create(
                    account_assign_cat=save_accasscats['account_assign_cat'],
                    defaults={'account_assign_cat': save_accasscats['account_assign_cat'],
                              'description': save_accasscats['description'],
                              'account_assignment_category_created_at': created_time_val,
                              'account_assignment_category_created_by': created_by_val,
                              'account_assignment_category_changed_at': changed_at_val,
                              'account_assignment_category_changed_by': changed_by_val,
                              'del_ind': False}, )

        Upload_response = list(
            AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat', 'description'))
        return Upload_response, MSG112, MSG113

    if Table == 'NumberRanges':

        for save_number_range in basic_data:
            if save_number_range['del_ind']:
                NumberRanges.objects.filter(sequence=save_number_range['sequence']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(NumberRanges, {
                    'sequence': save_number_range['sequence'], 'del_ind': False}, 'number_ranges_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(NumberRanges, {
                    'sequence': save_number_range['sequence'], 'del_ind': False}, 'number_ranges_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                guid = save_number_range['guid']
                #  If guid is empty create number range or update existing number range
                if guid == '':
                    guid = guid_generator()

                if not (NumberRanges.objects.filter(sequence=save_number_range['sequence'],
                                                    starting=save_number_range['starting'],
                                                    ending=save_number_range['ending'],
                                                    current=save_number_range['current'],
                                                    client=client,
                                                    document_type=DocumentType.objects.get
                                                        (document_type=save_number_range['document_type']),
                                                    del_ind=False).exists()):
                    obj, created = NumberRanges.objects.update_or_create(sequence=save_number_range['sequence'],
                                                                         document_type=DocumentType.objects.get
                                                                         (document_type=save_number_range[
                                                                             'document_type']),
                                                                         defaults={
                                                                             'sequence': save_number_range['sequence'],
                                                                             'starting': save_number_range[
                                                                                 'starting'],
                                                                             'ending': save_number_range[
                                                                                 'ending'],
                                                                             'current': save_number_range[
                                                                                 'current'],
                                                                             'client': OrgClients.objects.get
                                                                             (client=client),
                                                                             'document_type': DocumentType.objects.get
                                                                             (document_type=save_number_range
                                                                             ['document_type']),
                                                                             'guid': guid,
                                                                             'number_ranges_created_at': created_time_val,
                                                                             'number_ranges_created_by': created_by_val,
                                                                             'number_ranges_changed_at': changed_at_val,
                                                                             'number_ranges_changed_by': changed_by_val,
                                                                             'del_ind': False}, )

        Upload_response = list(
            NumberRanges.objects.filter(del_ind=False).values('sequence', 'starting', 'ending', 'current', 'guid'))
        return Upload_response, MSG112, MSG113

    if Table == 'TransactionTypes':

        for save_transaction_types in basic_data:

            if save_transaction_types['del_ind']:
                TransactionTypes.objects.filter(guid=save_transaction_types['guid']).update(
                    del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(TransactionTypes, {
                    'guid': save_transaction_types['guid'], 'del_ind': False}, 'transaction_types_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(TransactionTypes, {
                    'guid': save_transaction_types['guid'], 'del_ind': False}, 'transaction_types_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                # Below logic is for existing records changed.

                # Check if there is any change in the record if no then skip the record
                if (TransactionTypes.objects.filter(guid=save_transaction_types['guid'],
                                                    document_type=save_transaction_types['document_type'],
                                                    transaction_type=save_transaction_types['transaction_type'],
                                                    description=save_transaction_types['description'],
                                                    sequence=save_transaction_types['sequence'],
                                                    active_inactive=save_transaction_types['active_inactive'],
                                                    client=client).exists()):
                    continue

                elif not (TransactionTypes.objects.filter(
                        document_type=save_transaction_types['document_type'],
                        transaction_type=save_transaction_types['transaction_type'],
                        description=save_transaction_types['description'],
                        sequence=save_transaction_types['sequence'],
                        active_inactive=save_transaction_types['active_inactive'],
                        client=client).exists()):

                    if (TransactionTypes.objects.filter(client=client,
                                                        transaction_type=save_transaction_types['transaction_type'],

                                                        ).exists()):
                        TransactionTypes.objects.filter(transaction_type=save_transaction_types['transaction_type'],
                                                        client=client).update(
                            document_type=DocumentType.objects.get(
                                document_type=save_transaction_types['document_type']),
                            transaction_type=save_transaction_types['transaction_type'],
                            description=save_transaction_types['description'],
                            sequence=save_transaction_types['sequence'],
                            active_inactive=save_transaction_types['active_inactive'],
                            del_ind=False,
                            client=OrgClients.objects.get(client=client),
                            transaction_types_created_at=created_time_val,
                            transaction_types_created_by=created_by_val,
                            transaction_types_changed_at=changed_at_val,
                            transaction_types_changed_by=changed_by_val
                        )

                    else:
                        save_transaction_types['guid'] = 'GUID'

                # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.

                if save_transaction_types['guid'] == 'GUID':
                    obj, created = TransactionTypes.objects.get_or_create(
                        guid=guid_generator(),
                        document_type=DocumentType.objects.get(document_type=save_transaction_types['document_type']),
                        transaction_type=save_transaction_types['transaction_type'],
                        description=save_transaction_types['description'],
                        sequence=save_transaction_types['sequence'],
                        active_inactive=save_transaction_types['active_inactive'],
                        del_ind=False,
                        client=OrgClients.objects.get(client=client),
                        transaction_types_created_at=created_time_val,
                        transaction_types_created_by=created_by_val,
                        transaction_types_changed_at=changed_at_val,
                        transaction_types_changed_by=changed_by_val,
                    )

        upload_data_accounting_desc = list(TransactionTypes.objects.filter(del_ind=False).values('guid',
                                                                                                 'document_type',
                                                                                                 'description',
                                                                                                 'sequence',
                                                                                                 'active_inactive'))

        return upload_data_accounting_desc, MSG112, MSG113

    if Table == 'MessagesId':

        for save_messages in basic_data:
            if save_messages['del_ind']:
                if MessagesId.objects.filter(messages_id=save_messages['message_id']).exists():
                    # MessagesId.objects.filter(messages_id=save_messages['message_id']).update(
                    #     del_ind=True)
                    MessagesId.objects.filter(msg_id_guid=save_messages['msg_id_guid']).update(
                        del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(MessagesId, {
                    'messages_id': save_messages['message_id'], 'del_ind': False}, 'messages_id_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(MessagesId, {
                    'messages_id': save_messages['message_id'], 'del_ind': False}, 'messages_id_created_by')

                log_values = update_log_info(created_at_val, created_by_val)
                msg_id_guid = save_messages['msg_id_guid']

                if msg_id_guid == '':
                    msg_id_guid = guid_generator()

                MessagesId.objects.update_or_create(msg_id_guid=msg_id_guid,
                                                    messages_id=save_messages['message_id'],
                                                    defaults={
                                                        'msg_id_guid': msg_id_guid,
                                                        'messages_id': save_messages['message_id'],
                                                        'messages_type': save_messages['message_type'],
                                                        'del_ind': False,
                                                        'messages_id_created_by': log_values['created_by_val'],
                                                        'messages_id_changed_by': log_values['changed_by_val'],
                                                        'client': OrgClients.objects.get(client=client)
                                                    })

        Upload_response = list(
            MessagesId.objects.filter(del_ind=False).values('msg_id_guid', 'messages_id', 'messages_type'))

        return Upload_response, MSG112, MSG113

    if Table == 'MessagesIdDesc':

        for save_messages_desc in basic_data:
            if save_messages_desc['del_ind']:
                MessagesIdDesc.objects.filter(msg_id_desc_guid=save_messages_desc['msg_id_desc_guid']).update(
                    del_ind=True)
            else:
                msg_id_desc_guid = save_messages_desc['msg_id_desc_guid']

                if msg_id_desc_guid == '':
                    msg_id_desc_guid = guid_generator()

                created_at_val = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
                    'msg_id_desc_guid': save_messages_desc['msg_id_desc_guid'], 'del_ind': False},
                                                                                      'messages_id_desc_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
                    'msg_id_desc_guid': save_messages_desc['msg_id_desc_guid'], 'del_ind': False},
                                                                                      'messages_id_desc_created_by')

                log_values = update_log_info(created_at_val, created_by_val)

                # if not (MessagesIdDesc.objects.filter(msg_id_desc_guid=msg_id_desc_guid,
                #                                        del_ind=False,
                #                                       client=OrgClients.objects.get(client=client)).exists()):
                MessagesIdDesc.objects.update_or_create(msg_id_desc_guid=msg_id_desc_guid,
                                                        defaults={
                                                            'msg_id_desc_guid': msg_id_desc_guid,
                                                            'messages_id': save_messages_desc['messages_id'],
                                                            'messages_id_desc': save_messages_desc['messages_desc'],
                                                            'language_id': Languages.objects.get(
                                                                language_id=save_messages_desc['language_id']),
                                                            'del_ind': False,
                                                            'messages_id_desc_created_by': log_values[
                                                                'created_by_val'],
                                                            'messages_id_desc_changed_by': log_values[
                                                                'changed_by_val'],
                                                            'client': client
                                                        })

        Upload_response = list(
            MessagesIdDesc.objects.filter(del_ind=False, client=client).values('msg_id_desc_guid', 'messages_id',
                                                                               'messages_id_desc',
                                                                               'language_id'))

        return Upload_response, MSG112, MSG113

    if Table == 'upload_approval_type':

        for save_approval_type in basic_data:
            if save_approval_type['del_ind']:
                ApproverType.objects.filter(app_types=save_approval_type['app_types']).update(del_ind=True)
            else:
                created_at_val = django_query_instance.django_filter_value_list_query(ApproverType, {
                    'app_types': save_approval_type['app_types'], 'del_ind': False}, 'approver_type_created_at')
                created_by_val = django_query_instance.django_filter_value_list_query(ApproverType, {
                    'app_types': save_approval_type['app_types'], 'del_ind': False}, 'approver_type_created_by')

                if created_at_val and created_at_val[0] != '' and created_at_val[0] is not None:
                    created_time_val = created_at_val[0].strftime("%Y-%m-%d %H:%M:%S")
                    changed_at_val = datetime.today()
                    changed_by_val = global_variables.GLOBAL_LOGIN_USERNAME
                    created_by_val = created_by_val[0]
                else:
                    created_time_val = datetime.today()
                    changed_at_val = None
                    changed_by_val = None
                    created_by_val = global_variables.GLOBAL_LOGIN_USERNAME

                # print(update_log_info(created_at_val, created_by_val))

                if not (ApproverType.objects.filter(app_types=save_approval_type['app_types'],
                                                    appr_type_desc=save_approval_type['appr_type_desc'],
                                                    del_ind=False).exists()):
                    obj, created = ApproverType.objects.update_or_create(
                        app_types=save_approval_type['app_types'],
                        defaults={'app_types': save_approval_type['app_types'],
                                  'appr_type_desc': save_approval_type['appr_type_desc'],
                                  'approver_type_created_at': created_time_val,
                                  'approver_type_created_by': created_by_val,
                                  'approver_type_changed_at': changed_at_val,
                                  'approver_type_changed_by': changed_by_val,
                                  'del_ind': False,
                                  },
                    )

        Upload_response = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))

        return Upload_response, MSG112, MSG113


class SystemSettingConfig:
    def __init__(self, client):
        self.client = client

    def update_system_attributes(self, sys_attr_value, sys_attr_type):
        django_query_instance.django_filter_only_query(SystemSettingsConfig, {
            'client': self.client, 'del_ind': False, 'sys_attr_value': sys_attr_value, 'sys_attr_type': sys_attr_type
        }).update(sys_settings_default_flag=True)


def save_documenttype_data_into_db(documenttype_data):
    documenttype_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    doc_type_field = ''
    if documenttype_data['action'] == CONST_ACTION_DELETE:
        for documenttype_detail in documenttype_data['data']:
            doc_type_field = documenttype_detail['document_type']
            django_query_instance.django_update_query(DocumentType,
                                                      {'document_type': documenttype_detail['document_type']},
                                                      {'del_ind': True,
                                                       'document_type_changed_at': datetime.datetime.now(),
                                                       'document_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})

        fieldtypedesc_instance.reset_usedFlag(doc_type_field)
        message = MSG113
    else:
        for documenttype_detail in documenttype_data['data']:
            # if entry is not exists in db
            doc_type_field = documenttype_detail['document_type']
            if not django_query_instance.django_existence_check(DocumentType,
                                                                {'document_type': documenttype_detail[
                                                                    'document_type']}):
                documenttype_db_dictionary = {'document_type': (documenttype_detail['document_type']).upper(),
                                              'document_type_desc': convert_to_camel_case(documenttype_detail['document_type_desc']),
                                              'document_type_created_at': datetime.datetime.now(),
                                              'document_type_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                              'document_type_changed_at': datetime.datetime.now(),
                                              'document_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME}
                documenttype_db_list.append(documenttype_db_dictionary)
            else:
                django_query_instance.django_update_query(DocumentType,
                                                          {'document_type': documenttype_detail['document_type']},
                                                          {'document_type': documenttype_detail['document_type'],
                                                           'document_type_desc': convert_to_camel_case(documenttype_detail[
                                                               'document_type_desc']),
                                                           'document_type_changed_at': datetime.datetime.now(),
                                                           'document_type_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})
        bulk_create_entry_db(DocumentType, documenttype_db_list)
        fieldtypedesc_instance.update_usedFlag(doc_type_field)
        message = MSG112
    upload_response = get_configuration_data(DocumentType, {'del_ind': False},
                                             ['document_type', 'document_type_desc'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'document_type'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_transactiontype_data_into_db(transactiontype_data):
    transactiontype_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    active_inactive_field = ''
    doc_type = ''
    client = global_variables.GLOBAL_CLIENT
    if transactiontype_data['action'] == CONST_ACTION_DELETE:
        for transactiontype_detail in transactiontype_data['data']:
            doc_type = transactiontype_detail['document_type']
            active_inactive_field = transactiontype_detail['active_inactive']
            if not django_query_instance.django_existence_check(OrgAttributesLevel,
                                                            {'client': global_variables.GLOBAL_CLIENT,
                                                             'low': transactiontype_detail['transaction_type'],
                                                             'del_ind': False,
                                                             'attribute_id':CONST_SC_TRANS_TYPE}):
                django_query_instance.django_update_query(TransactionTypes,
                                                          {'transaction_type': transactiontype_detail['transaction_type']},
                                                          {'del_ind': True,
                                                           'transaction_types_changed_at': datetime.datetime.now(),
                                                           'transaction_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
                fieldtypedesc_instance.reset_usedFlag(active_inactive_field)
        message = MSG113
    else:
        for transactiontype_detail in transactiontype_data['data']:
            doc_type = transactiontype_detail['document_type']
            active_inactive_field = transactiontype_detail['active_inactive']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(TransactionTypes,
                                                                {'transaction_type': transactiontype_detail[
                                                                    'transaction_type'],
                                                                 'sequence': transactiontype_detail['sequence']
                                                                 }):
                guid = guid_generator()
                transactiontype_db_dictionary = {'guid': guid,
                                                 'transaction_type': (transactiontype_detail['transaction_type']).upper(),
                                                 'description': convert_to_camel_case(transactiontype_detail['description']),
                                                 'sequence': transactiontype_detail['sequence'],
                                                 'active_inactive': transactiontype_detail['active_inactive'],
                                                 'document_type': DocumentType.objects.get(
                                                     document_type=transactiontype_detail['document_type']),
                                                 'del_ind': False,
                                                 'client': client,
                                                 'transaction_types_created_at': datetime.datetime.now(),
                                                 'transaction_types_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                 'transaction_types_changed_at': datetime.datetime.now(),
                                                 'transaction_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                 }
                transactiontype_db_list.append(transactiontype_db_dictionary)
            else:
                delete_flag = True
                if django_query_instance.django_existence_check(OrgAttributesLevel,
                                                                    {'client': global_variables.GLOBAL_CLIENT,
                                                                     'low': transactiontype_detail['transaction_type'],
                                                                     'del_ind': False,
                                                                     'attribute_id': CONST_SC_TRANS_TYPE}):
                    delete_flag = False
                if delete_flag:
                    django_query_instance.django_update_query(TransactionTypes,
                                                              {'transaction_type': transactiontype_detail[
                                                                  'transaction_type'],'sequence': transactiontype_detail['sequence']},
                                                              {'transaction_type': transactiontype_detail[
                                                                   'transaction_type'],
                                                               'description': convert_to_camel_case(transactiontype_detail[
                                                                   'description']),
                                                               'sequence': transactiontype_detail['sequence'],
                                                               'active_inactive': transactiontype_detail['active_inactive'],
                                                               'document_type': DocumentType.objects.get(
                                                                   document_type=transactiontype_detail['document_type']),
                                                               'transaction_types_changed_at': datetime.datetime.now(),
                                                               'transaction_types_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                               'client': client,
                                                               'del_ind': False})
        bulk_create_entry_db(TransactionTypes,transactiontype_db_list)
        fieldtypedesc_instance.update_usedFlag(active_inactive_field)
        message = MSG112
    upload_response = get_configuration_data(TransactionTypes, {'del_ind': False,'document_type':doc_type,
                                                                'client':global_variables.GLOBAL_CLIENT},
                                             ['guid', 'transaction_type', 'description', 'document_type','sequence',
                                              'active_inactive'])

    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'document_type'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message,upload_fieldtypedesc


def save_calendar_data_into_db(calendar_data):
    """

    """
    calendar_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if calendar_data['action'] == CONST_ACTION_DELETE:
        for calendar_detail in calendar_data['data']:
            django_query_instance.django_update_query(CalenderConfig,
                                                      {'calender_id': calendar_detail['calender_id']},
                                                      {'del_ind': True,
                                                       'calender_config_changed_at': datetime.datetime.now(),
                                                       'calender_config_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for calendar_detail in calendar_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(CalenderConfig,
                                                                {'calender_id': calendar_detail[
                                                                    'calender_id']
                                                                 }):
                guid = guid_generator()
                calenderid = random_int(4)
                print(calenderid)
                calendar_db_dictionary = {'calender_config_guid': guid,
                                          'calender_id': calenderid,
                                          'description': convert_to_camel_case(calendar_detail['description']),
                                          'year': calendar_detail['year'],
                                          'working_days': calendar_detail['working_days'],
                                          'del_ind': False,
                                          'client': client,
                                          'country_code': Country.objects.get(country_code=calendar_detail['country']),
                                          'calender_config_created_at': datetime.datetime.now(),
                                          'calender_config_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                          'calender_config_changed_at': datetime.datetime.now(),
                                          'calender_config_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                          }
                calendar_db_list.append(calendar_db_dictionary)
            else:
                django_query_instance.django_update_query(CalenderConfig,
                                                          {'calender_id': calendar_detail[
                                                              'calender_id']},
                                                          {'calender_id': calendar_detail['calender_id'],
                                                           'description': convert_to_camel_case(calendar_detail['description']),
                                                           'year': calendar_detail['year'],
                                                           'working_days': calendar_detail['working_days'],
                                                           'country_code': Country.objects.get(
                                                               country_code=calendar_detail['country']),
                                                           'calender_config_changed_at': datetime.datetime.now(),
                                                           'calender_config_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})

        bulk_create_entry_db(CalenderConfig, calendar_db_list)
        message = MSG112
    upload_response = get_configuration_data(CalenderConfig, {'del_ind': False},
                                             ['calender_config_guid', 'calender_id', 'description',
                                              'year', 'working_days', 'country_code'])
    return upload_response, message


def save_calendarholiday_data_into_db(calendar_data):
    """

    """
    calendar_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if calendar_data['action'] == CONST_ACTION_DELETE:
        for calendar_detail in calendar_data['data']:
            django_query_instance.django_update_query(CalenderHolidays,
                                                      {'calender_holiday_guid': calendar_detail[
                                                          'calender_holiday_guid']},
                                                      {'del_ind': True,
                                                       'changed_at': datetime.datetime.now(),
                                                       'changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for calendar_detail in calendar_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(CalenderHolidays,
                                                                {'calender_holiday_guid': calendar_detail[
                                                                    'calender_holiday_guid']}):
                guid = guid_generator()
                calendar_db_dictionary = {'calender_holiday_guid': guid,
                                          'calender_id': calendar_detail['calender_id'],
                                          'holiday_description': convert_to_camel_case(calendar_detail['holiday_description']),
                                          'from_date': calendar_detail['from_date'],
                                          'to_date': calendar_detail['to_date'],
                                          'del_ind': False,
                                          'client': client,
                                          'created_at': datetime.datetime.now(),
                                          'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                          'changed_at': datetime.datetime.now(),
                                          'changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                          }
                calendar_db_list.append(calendar_db_dictionary)
            else:
                django_query_instance.django_update_query(CalenderHolidays,
                                                          {'calender_holiday_guid': calendar_detail[
                                                              'calender_holiday_guid']},
                                                          {'calender_holiday_guid': calendar_detail[
                                                              'calender_holiday_guid'],
                                                           'calender_id': calendar_detail['calender_id'],
                                                           'holiday_description': convert_to_camel_case(calendar_detail[
                                                               'holiday_description']),
                                                           'from_date': calendar_detail['from_date'],
                                                           'to_date': calendar_detail['to_date'],
                                                           'changed_at': datetime.datetime.now(),
                                                           'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'client': client,
                                                           'del_ind': False})
        bulk_create_entry_db(CalenderHolidays, calendar_db_list)
        message = MSG112
    upload_response = get_configuration_data(CalenderHolidays, {'del_ind': False},
                                             ['calender_holiday_guid', 'calender_id', 'holiday_description',
                                              'from_date', 'to_date'])
    return upload_response, message


def save_actasmt_data_into_db(accasscat_data):
    """

    """
    accasscat_db_list = []
    fieldtypedesc_instance = FieldTypeDescription()
    acct_assmt_field = ''
    if accasscat_data['action'] == CONST_ACTION_DELETE:
        for accasscat_detail in accasscat_data['data']:
            acct_assmt_field = accasscat_detail['account_assign_cat']
            django_query_instance.django_update_query(AccountAssignmentCategory,
                                                      {'account_assign_cat': accasscat_detail['account_assign_cat']},
                                                      {'del_ind': True,
                                                       'account_assignment_category_changed_at': datetime.datetime.now(),
                                                       'account_assignment_category_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
            fieldtypedesc_instance.reset_usedFlag(acct_assmt_field)
        message = MSG113
    else:
        for accasscat_detail in accasscat_data['data']:
            acct_assmt_field = accasscat_detail['account_assign_cat']
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(AccountAssignmentCategory,
                                                                {'account_assign_cat': accasscat_detail[
                                                                    'account_assign_cat']}):
                accasscat_db_dictionary = {'account_assign_cat': (accasscat_detail['account_assign_cat']).upper(),
                                           'description': convert_to_camel_case(accasscat_detail['description']),
                                           'del_ind': False,
                                           'account_assignment_category_created_at': datetime.datetime.now(),
                                           'account_assignment_category_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'account_assignment_category_changed_at': datetime.datetime.now(),
                                           'account_assignment_category_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                           }
                accasscat_db_list.append(accasscat_db_dictionary)
            else:
                django_query_instance.django_update_query(AccountAssignmentCategory,
                                                          {'account_assign_cat': accasscat_detail[
                                                              'account_assign_cat']},
                                                          {'account_assign_cat': accasscat_detail[
                                                              'account_assign_cat'],
                                                           'description': convert_to_camel_case(accasscat_detail['description']),
                                                           'account_assignment_category_changed_at': datetime.datetime.now(),
                                                           'account_assignment_category_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False})
        bulk_create_entry_db(AccountAssignmentCategory, accasscat_db_list)
        fieldtypedesc_instance.update_usedFlag(acct_assmt_field)
        message = MSG112
    upload_response = get_configuration_data(AccountAssignmentCategory, {'del_ind': False},
                                             ['account_assign_cat', 'description'])
    upload_fieldtypedesc = fieldtypedesc_instance.get_field_type_desc_values(FieldTypeDesc,
                                                                             {'del_ind': False, 'used_flag': False,
                                                                              'field_name': 'acct_assignment_category'},
                                                                             ['field_type_id', 'field_type_desc'])

    return upload_response, message, upload_fieldtypedesc


def save_messageId_data_into_db(messageId_data):
    """

    """
    messageId_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if messageId_data['action'] == CONST_ACTION_DELETE:
        for messageId_detail in messageId_data['data']:
            django_query_instance.django_update_query(MessagesId,
                                                      {'messages_id': messageId_detail['message_id']},
                                                      {'del_ind': True,
                                                       'messages_id_changed_at': datetime.datetime.now(),
                                                       'messages_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for messageId_detail in messageId_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(MessagesId,
                                                                {'messages_id': messageId_detail[
                                                                    'message_id']}):
                guid = guid_generator()
                messageId_db_dictionary = {'msg_id_guid': guid,
                                           'messages_id': messageId_detail['message_id'],
                                           'messages_type': messageId_detail['message_type'],
                                           'del_ind': False,
                                           'client': client,
                                           'messages_id_created_at': datetime.datetime.now(),
                                           'messages_id_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                           'messages_id_changed_at': datetime.datetime.now(),
                                           'messages_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                           }
                messageId_db_list.append(messageId_db_dictionary)
            else:
                django_query_instance.django_update_query(MessagesId,
                                                          {'messages_id': messageId_detail[
                                                              'message_id']},
                                                          {'messages_id': messageId_detail['message_id'],
                                                           'messages_type': messageId_detail['message_type'],
                                                           'messages_id_changed_at': datetime.datetime.now(),
                                                           'messages_id_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False,
                                                           'client': client})
        bulk_create_entry_db(MessagesId, messageId_db_list)
        message = MSG112
    upload_response = get_configuration_data(MessagesId, {'del_ind': False},
                                             ['msg_id_guid', 'messages_id', 'messages_type'])
    return upload_response, message


def save_messageIdDesc_data_into_db(messageIdDesc_data):
    """

    """
    messageIdDesc_db_list = []
    client = global_variables.GLOBAL_CLIENT
    if messageIdDesc_data['action'] == CONST_ACTION_DELETE:
        for messageIdDesc_detail in messageIdDesc_data['data']:
            django_query_instance.django_update_query(MessagesIdDesc,
                                                      {'messages_id': messageIdDesc_detail['messages_id'],
                                                       'language_id': messageIdDesc_detail['language_id']
                                                        },
                                                      {'del_ind': True,
                                                       'messages_id_desc_changed_at': datetime.datetime.now(),
                                                       'messages_id_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME})
        message = MSG113
    else:
        for messageIdDesc_detail in messageIdDesc_data['data']:
            # if entry is not exists in db
            if not django_query_instance.django_existence_check(MessagesIdDesc,
                                                                {'messages_id': messageIdDesc_detail[
                                                                    'messages_id'],
                                                                 'language_id': messageIdDesc_detail['language_id']
                                                                 }):
                guid = guid_generator()
                messageIdDesc_db_dictionary = {'msg_id_desc_guid': guid,
                                               'messages_id': messageIdDesc_detail['messages_id'],
                                               'messages_id_desc': convert_to_camel_case(messageIdDesc_detail['message_id_desc']),
                                               'language_id': Languages.objects.get(
                                                   language_id=messageIdDesc_detail['language_id']),
                                               'del_ind': False,
                                               'client': client,
                                               'messages_id_desc_created_at': datetime.datetime.now(),
                                               'messages_id_desc_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                               'messages_id_desc_changed_at': datetime.datetime.now(),
                                               'messages_id_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME
                                               }
                messageIdDesc_db_list.append(messageIdDesc_db_dictionary)
            else:
                django_query_instance.django_update_query(MessagesIdDesc,
                                                          {'messages_id': messageIdDesc_detail[
                                                              'messages_id'],
                                                           'language_id': messageIdDesc_detail['language_id']
                                                           },
                                                          {'messages_id': messageIdDesc_detail['messages_id'],
                                                           'messages_id_desc': convert_to_camel_case(messageIdDesc_detail['message_id_desc']),
                                                           'language_id': Languages.objects.get(
                                                               language_id=messageIdDesc_detail['language_id']),
                                                           'messages_id_desc_changed_at': datetime.datetime.now(),
                                                           'messages_id_desc_changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                           'del_ind': False,
                                                           'client': client})
        bulk_create_entry_db(MessagesIdDesc, messageIdDesc_db_list)
        message = MSG112
    upload_response = get_configuration_data(MessagesIdDesc, {'del_ind': False},
                                             ['msg_id_desc_guid', 'messages_id', 'messages_id_desc', 'language_id'])
    return upload_response, message

