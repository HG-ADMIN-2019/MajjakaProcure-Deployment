from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import transaction
from django.http import JsonResponse

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_SC_APPR_APPROVED, CONST_SC_HEADER_APPROVED, CONST_COMPLETED
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG184
from eProc_Doc_Search.views import generate_sc_details_pdf
from eProc_Emails.Utilities.email_notif_generic import appr_notify
from eProc_Generate_PDF.Utilities.generate_pdf_generic import save_pdf
from eProc_Purchase_Order.Utilities.purchase_order_generic import CreatePurchaseOrder, create_po_pdf
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Shopping_Cart.models import ScHeader
from eProc_Workflow.Utilities.work_flow_specific import update_appr_status

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


@transaction.atomic
def save_appr_status(request):
    """
    save approval status
    :param request:
    :return:
    """
    data = {}
    appr_status = JsonParser_obj.get_json_from_req(request)
    variant_name = 'SC_APPROVAL'
    client = getClients(request)
    update_user_info(request)
    header_status, sc_header_instance = update_appr_status(appr_status)
    if header_status == CONST_SC_HEADER_APPROVED:
        create_purchase_order = CreatePurchaseOrder(sc_header_instance)
        create_purchase_order.create_po()

    # approval_detail = appr_status['status'].split('-')
    # header_guid = approval_detail[1]
    # sc_header_instance = django_query_instance.django_get_query(ScHeader, {'guid': header_guid})
    ## generate_sc_details_pdf(request, doc_number)
    # -------------------------------------------------------------
    # context = create_po_pdf(sc_header_instance.doc_number)
    # file_name,status,output = save_pdf(context)
    # if not status:
    #     return JsonResponse({'status': 400})
    # mail = EmailMultiAlternatives('subject', 'text_content', settings.EMAIL_HOST_USER, ['deepika@hiranya-garbha.com'])
    # file = open(output, "r+")
    # attachment = file.read()
    # file.close()
    # mail.attach("my.pdf", attachment, "application/pdf")
    # mail.send()
    # return JsonResponse({'status':200,'path':f'/media/{sc_header_instance.doc_number}.pdf'})

    data['message'] = MSG184
    return JsonResponse(data)
