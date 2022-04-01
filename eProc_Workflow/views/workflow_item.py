from django.db import transaction
from django.http import JsonResponse
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.messages.messages import MSG184
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Workflow.Utilities.work_flow_specific import update_appr_status

JsonParser_obj = JsonParser()


@transaction.atomic
def save_appr_status(request):
    """
    save approval status
    :param request:
    :return:
    """
    data = {}
    appr_status = JsonParser_obj.get_json_from_req(request)
    update_user_info(request)
    update_appr_status(appr_status)
    data['message'] = MSG184
    return JsonResponse(data)
