from re import sub

from eProc_Attributes.models.org_attribute_models import OrgAttributesLevel
from eProc_Basic.Utilities.constants.constants import CONST_SC_TRANS_TYPE
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import FieldTypeDesc, TransactionTypes

django_query_instance = DjangoQueries()


def get_configuration_data(db_name, filter_query, value_list):
    """

    """
    result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
    return result


class FieldTypeDescription:
    @staticmethod
    def update_usedFlag(field_type_id):
        django_query_instance.django_filter_only_query(FieldTypeDesc, {
            'del_ind': False, 'field_type_id': field_type_id
        }).update(used_flag=True)

    @staticmethod
    def reset_usedFlag(field_type_id):
        django_query_instance.django_filter_only_query(FieldTypeDesc, {
            'del_ind': False, 'field_type_id': field_type_id
        }).update(used_flag=False)

    @staticmethod
    def get_field_type_desc_values(db_name, filter_query, value_list):
        result = django_query_instance.django_filter_query(db_name, filter_query, None, value_list)
        return result

