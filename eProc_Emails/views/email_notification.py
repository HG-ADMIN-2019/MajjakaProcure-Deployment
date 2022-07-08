"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    email_notification.py
Usage:
    On click of E-mail notification tab in Admin tool
    email_notification_form - This function handles the display, modifying and saving the email notification format and renders emailnotif.html
Author:
     Siddarth
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Add_Item.views import JsonParser_obj
from eProc_Basic.Utilities.constants.constants import CONST_USER_REG
from eProc_Basic.Utilities.functions.django_q_query import django_q_query
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import NotifSettings, NotifKeywordsDesc, NotifSettingsDesc, EmailObjectTypes, \
    EmailKeywords, EmailContents
from eProc_Emails.Utilities.email_notif_generic import email_notify
from eProc_Emails.models import EmailUserMonitoring
from eProc_Registration.models import UserData

django_query_instance = DjangoQueries()


@login_required
def email_notification_form(req):
    """
    handles email notification data for displaying, edit and saving
    :param req: request data from UI
    :return: renders emailnotif.html
    """
    client = getClients(req)
    variant_list = []
    keyword_list = []

    django_query_instance.django_filter_only_query(EmailObjectTypes, {'client': client, 'del_ind': False})
    object_type_data = django_query_instance.django_filter_only_query(EmailObjectTypes,
                                                                      {'client': client,
                                                                       'del_ind': False}).values('object_type')

    for variant_names in object_type_data:
        variant_list.append(variant_names['object_type'])
    try:
        keyword_data = django_query_instance.django_filter_only_query(EmailKeywords, {
            'client': client,
            'del_ind': False
        }).values('keyword')
        for dt in keyword_data:
            keyword_list.append(dt['keyword'])

        form_data = django_query_instance.django_filter_only_query(EmailContents, {
            'object_type': variant_list[0],
            'client': client,
            'del_ind': False
        })
        data_onload = list(form_data)

    except ObjectDoesNotExist:
        msg = messages.error(req, 'please maintain data')
        return render(req, 'emailnotif.html', msg)

    context = {
        'variant_list': variant_list,
        'keyword_list': keyword_list,
        'form_data': form_data,
        'data_onload': data_onload,
        'inc_nav': True,
        'inc_shop_nav': True,
        'is_slide_menu': True
    }

    return render(req, 'emailnotif.html', context)


@transaction.atomic
def edit_email_notif_form(req):
    """
    Function to retrieve selected email notification type data.
    :param req:
    :return:
    """
    client = getClients(req)

    if req.is_ajax():
        keyword_list = []
        selected_variant = req.POST.get('variant_data')

        form_data1 = django_query_instance.django_get_query(EmailContents,
                                                            {'object_type': selected_variant, 'client': client,
                                                             'del_ind': False})

        keyword_data1 = django_query_instance.django_filter_only_query(EmailKeywords,
                                                                       {'object_type': selected_variant,
                                                                        'client': client, 'del_ind': False}).values(
            'keyword')

        for keywords in keyword_data1:
            keyword_list.append(keywords['keyword'])

        ajax_context = {
            'keyword_list': keyword_list,
            'email_contents_guid': form_data1.email_contents_guid,
            'subject': form_data1.subject,
            'body': form_data1.body,
            'header': form_data1.header,
            'footer': form_data1.footer
        }

        return JsonResponse(ajax_context)


@transaction.atomic
def update_email_notif_form(request):
    """
    This function is to update the edited email content data.
    :param request:
    :return:
    """
    if request.method == 'POST':
        update_email_guid = request.POST.get('email_guid')
        update_email_subject = request.POST.get('email_subject')
        update_email_header = request.POST.get('email_header')
        update_email_body = request.POST.get('email_body')
        update_email_footer = request.POST.get('email_footer')

        if update_email_guid is None:
            update_email_guid = guid_generator()
        update_email_notif_data = django_query_instance.django_filter_only_query(EmailContents,
                                                                                 {
                                                                                     'email_contents_guid': update_email_guid,
                                                                                     'del_ind': False})

        update_email_notif_data.update(subject=update_email_subject, header=update_email_header, body=update_email_body,
                                       footer=update_email_footer)

        return JsonResponse({'message': MSG037})


@transaction.atomic
def resend_user_mail(request):
    """
    This function is to update the edited email content data.
    :param request:
    :return:
    """
    global message
    variant_name = CONST_USER_REG
    client = getClients(request)
    basic_data = JsonParser_obj.get_json_from_req(request)

    # for user in user_details:
    #     first_name = user['first_name']
    #     last_name = user['last_name']

    if request.is_ajax():
        for val in basic_data:
            username = val['username']
            email = val['email']
            email_user_monitoring_guid = val['email_user_monitoring_guid']
            user_details = django_query_instance.django_get_query(UserData, {'email': val['email'],
                                                                             'del_ind': False,
                                                                             'client': client})
            email_data = {
                'username': username,
                'email': email,
                'email_user_monitoring_guid': email_user_monitoring_guid,
                'first_name': user_details.first_name
            }
            status = email_notify(email_data, variant_name, client)
            if status == 1:
                message = "Email Re-Sent Successfully"
            else:
                message = "Email Not-Sent"
            email_list = django_query_instance.django_filter_query(EmailUserMonitoring,
                                                                   {'client': global_variables.GLOBAL_CLIENT,
                                                                    'object_type': 'REGISTRATION',
                                                                    'email_status': 2,
                                                                    'del_ind': False}, None, None)

    return JsonResponse({'message': message, 'email_list': email_list})
