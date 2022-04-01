from django.http import JsonResponse

from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import MessagesIdDesc, MessagesId

django_query_instance = DjangoQueries()


# Function to get the message details
def get_message_description(request):
    if request.method == "POST" and request.is_ajax():
        msgid = JsonParser().get_json_from_req(request)
        client = global_variables.GLOBAL_CLIENT
        message_type = django_query_instance.django_filter_value_list_query(MessagesId, {
            'del_ind': False, 'messages_id': msgid, 'client': client,
        }, 'messages_type')
        message_desc = django_query_instance.django_filter_value_list_query(MessagesIdDesc, {
            'del_ind': False, 'messages_id': msgid, 'client': client,
        }, 'messages_id_desc')
        return JsonResponse({'messages_id_desc': message_desc, 'message_type': message_type})
