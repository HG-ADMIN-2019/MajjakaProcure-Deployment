from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_MY_ORDER
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_login_obj_id
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.decorators import authorize_view
from eProc_Doc_Search_and_Display.Doc_Search_Forms.search_forms import *
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_my_order_default, \
    get_sc_header_app, DocumentSearch
from eProc_Shopping_Cart.context_processors import update_user_info


@login_required
@authorize_view(CONST_MY_ORDER)
def sc_po_hdr_search(request):
    """
    :param request:
    :return:
    """

    inp_doc_type = ''
    result = ''
    page_range = 0
    approver_details = []
    sc_header = []
    sc_appr = []
    sc_completion = []
    encrypted_header_guid = []
    requester_first_name =''
    sc_completion_flag = False
    client = getClients(request)
    login_user_obj_id = get_login_obj_id(request)
    update_user_info(request)
    username = global_variables.GLOBAL_LOGIN_USERNAME

    inp_status = request.POST.getlist('status', default=None)
    if not request.method == 'POST':
        if 'results' in request.session:
            request.POST = request.session['results']
            request.method = 'POST'

    if request.method == 'POST':
        request.session['results'] = request.POST

    # If method is post get the form values and get header details accordingly
    if request.method == 'POST':
        requester = global_variables.GLOBAL_LOGIN_USERNAME
        created_by = global_variables.GLOBAL_LOGIN_USERNAME
        document_search_instance = DocumentSearch(requester, created_by)
        if settings.SEARCH_FORM == 'X':
            search_form = ExtSearch(request.POST)
        else:
            search_form = SearchForm(request.POST)
        if search_form.is_valid():
            inp_doc_type = request.POST.get('doc_type')
            inp_doc_num = request.POST.get('doc_num')
            # inp_from_date  = request.POST.get('from_date')
            # inp_to_date    = request.POST.get('to_date')
            inp_supl = request.POST.get('supplier')
            # inp_created_by = request.POST.get('created_by')
            # inp_requester  = request.POST.get('requester')
            inp_timeframe = request.POST.get('time_frame')
            inp_sc_name = request.POST.get('SCName')
            # inp_buy_on_behalf = request.POST.get('buy_on_behalf')
            search_criteria = document_search_instance.define_search_criteria({'document_number': inp_doc_num,
                                                                               'document_type': inp_doc_type,
                                                                               'supplier': inp_supl,
                                                                               'timeframe': inp_timeframe,
                                                                               'sc_name': inp_sc_name,
                                                                               'status': inp_status,
                                                                               'requester': username}, 'my_order')

            result = document_search_instance.get_header_details(search_criteria)

    else:
        if settings.SEARCH_FORM == 'X':
            search_form = ExtSearch()
        else:
            search_form = SearchForm()

    t_count = len(result)
    my_order_default = get_my_order_default(client, login_user_obj_id)

    if inp_doc_type == 'SC':
        # Appending SCHeader fields and its respective SCApproval
        sc_header, sc_appr, sc_completion,requester_first_name = get_sc_header_app(result, client)
    elif inp_doc_type == 'PO':
        for po_header_guid in result:
            array_init = [po_header_guid.guid, po_header_guid.created_at, po_header_guid.description,
                          po_header_guid.doc_number, po_header_guid.total_value, po_header_guid.currency,
                          po_header_guid.status, po_header_guid.created_by]
            approver_details.append(array_init)

    # Paginating search results and restricting the results to 50 per page
    page = request.GET.get('page', 1)
    paginator = Paginator(approver_details, 5)
    try:
        approver_details = paginator.page(page)
    except PageNotAnInteger:
        approver_details = paginator.page(1)
    except EmptyPage:
        approver_details = paginator.page(paginator.num_pages)

    for header_guid in sc_header:
        encrypted_header_guid.append(encrypt(header_guid['guid']))

    sc_header = zip(sc_header, encrypted_header_guid)

    # Context to display in search.html
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'sc_appr': sc_appr,
        'sc_header': sc_header,
        'sc_completion': sc_completion,
        'requester_first_name':requester_first_name,
        'sform': search_form,
        'results': result,
        'my_order_default': my_order_default,
        'approver_details': approver_details,
        'page_range': page_range,
        't_count': t_count,
        'inp_doc_type': inp_doc_type,
        'sc_completion_flag': sc_completion_flag,
        'inp_status': inp_status,
        'is_slide_menu': True,
        'is_shop_active': True
    }

    return render(request, 'Doc Search and Display/search.html', context)
