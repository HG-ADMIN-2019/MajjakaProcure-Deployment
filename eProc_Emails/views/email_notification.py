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
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import NotifSettings, NotifKeywordsDesc, NotifSettingsDesc

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
    django_query_instance.django_filter_only_query(NotifSettings, {'client': client, 'del_ind': False})
    variant_data = django_query_instance.django_filter_only_query(NotifSettings,
                                                                  {'client': client,
                                                                   'del_ind': False}).values('variant_name')

    for variant_names in variant_data:
        variant_list.append(variant_names['variant_name'])
    try:
        keyword_data = django_query_instance.django_filter_only_query(NotifKeywordsDesc, {
            'variant_name': 'user_reg',
            'client': client,
            'del_ind': False
        })

        form_data = django_query_instance.django_filter_only_query(NotifSettingsDesc, {
            'variant_name': 'user_reg',
            'client': client,
            'del_ind': False
        })

    except ObjectDoesNotExist:
        msg = messages.error(req, 'please maintain data')
        return render(req, 'emailnotif.html', msg)

    context = {
        'variant_list': variant_list,
        'keyword_data': keyword_data,
        'form_data': form_data,
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

        form_data1 = django_query_instance.django_get_query(NotifSettingsDesc,
                                                            {'variant_name': selected_variant, 'client': client,
                                                             'del_ind': False})

        keyword_data1 = django_query_instance.django_filter_only_query(NotifKeywordsDesc,
                                                                       {'variant_name': selected_variant,
                                                                        'client': client, 'del_ind': False}).values(
            'keyword')

        for keywords in keyword_data1:
            keyword_list.append(keywords['keyword'])

        ajax_context = {
            'keyword_list': keyword_list,
            'notif_guid': form_data1.notif_desc_guid,
            'notif_subject': form_data1.notif_subject,
            'notif_body': form_data1.notif_body
        }

        return JsonResponse(ajax_context)


@transaction.atomic
def update_email_notif_form(request):
    """
    This function is to update the edited email notification data.
    :param request:
    :return:
    """
    if request.method == 'POST':
        update_email_guid = request.POST.get('email_guid')
        update_email_subject = request.POST.get('email_subject')
        update_email_body = request.POST.get('email_body')
        update_email_notif_data = django_query_instance.django_filter_only_query(NotifSettingsDesc,
                                                                                 {'notif_desc_guid': update_email_guid,
                                                                                  'del_ind': False})

        update_email_notif_data.update(notif_subject=update_email_subject, notif_body=update_email_body)

        return JsonResponse({'message': MSG037})
