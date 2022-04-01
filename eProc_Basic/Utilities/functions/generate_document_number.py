from django.core.exceptions import ObjectDoesNotExist
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.messages.messages import MSG123
from eProc_Configuration.models import NumberRanges
from eProc_Configuration.models.development_data import TransactionTypes
from eProc_User_Settings.Utilities.user_settings_generic import get_attr_value

django_query_instance = DjangoQueries()


def generate_document_number(attr_id, client, object_id_list, edit_flag, doc_type):
    """
    :return:
    """
    user_attr_value = get_attr_value(client, attr_id, object_id_list, edit_flag)
    if len(user_attr_value) == 0:
        return False, MSG123

    try:
        get_sequence = django_query_instance.django_get_query(TransactionTypes, {'transaction_type': user_attr_value,
                                                                                 'client': client, 'del_ind': False,
                                                                                 'document_type': doc_type})

        if get_sequence is None:
            return False, 'Transaction types or Number Ranges has not been configured.Please contact your admin'

        get_sequence_range = django_query_instance.django_get_query(NumberRanges, {'sequence': get_sequence.sequence,
                                                                                   'client': client,
                                                                                   'document_type': doc_type})

    except ObjectDoesNotExist:
        return False, 'Transaction types or Number Ranges has not been configured.Please contact your admin'

    if get_sequence_range.current >= get_sequence_range.ending:
        return False, 'Number ranges exceeded.Please contact your admin'
    else:
        doc_number = int(get_sequence_range.current) + 1

    return doc_number, get_sequence_range.sequence, user_attr_value
