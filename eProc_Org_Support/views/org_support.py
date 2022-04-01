from aioredis.commands import transaction
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG155, MSG113, MSG156, MSG157
from eProc_Chat.Utitlities.doc_chat_specific import create_chat_participant
from eProc_Org_Support.models import OrgAnnouncements, OrgSupport
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.get_db_query import django_query_instance, get_login_obj_id
from eProc_Configuration.models.development_data import *
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.guid_generator import random_int, guid_generator
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData


def customer_support_chat(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    username = global_variables.GLOBAL_LOGIN_USERNAME

    if request.method == 'POST':
        customer_support_username_list = list(
            OrgSupport.objects.filter(org_support_types='CUSTOMER_SUPPORT', client=client, del_ind=False).values_list(
                'username', flat=True))
        customer_support_username_list.append(username)

        room_name = '12345'
        title = 'CUSTOMER_SUPPORT'
        chat_type = 'CUSTOMER_SUPPORT'

        create_chat_participant(customer_support_username_list, room_name, title, chat_type, client)
        return


def org_announcement_save(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    obj_id = django_query_instance.django_get_query(OrgModel, {
        'object_id': global_variables.GLOBAL_LOGIN_USER_OBJ_ID, 'del_ind': False
    })

    status_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'status'
    })
    priority_dropdown_values = django_query_instance.django_filter_only_query(FieldTypeDesc, {
        'del_ind': False, 'field_name': 'priority'
    })
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'status_dropdown_values': status_dropdown_values,
        'priority_dropdown_values': priority_dropdown_values,
    }

    if request.method == "POST" and request.is_ajax():
        org_announcement_data = JsonParser().get_json_from_req(request)

        announcement_num = org_announcement_data['announcement_id']
        if announcement_num == '':
            announcement_num = random_int(8)

        guid = org_announcement_data['announcement_guid']
        if guid == '':
            guid = guid_generator()

            defaults = {
                'unique_announcement_id': guid,
                'announcement_id': announcement_num,
                'announcement_subject': org_announcement_data['announcement_subject'],
                'announcement_description': org_announcement_data['announcement_description'],
                'status': org_announcement_data['status'],
                'priority': org_announcement_data['priority'],
                'announcement_from_date': org_announcement_data['announcement_from_date'],
                'announcement_to_date': org_announcement_data['announcement_to_date'],
                'client': client,
                'del_ind': False,
                'object_id': obj_id,
            }

            django_query_instance.django_update_or_create_query(OrgAnnouncements, {'unique_announcement_id': guid},
                                                                defaults)

        return JsonResponse({'message': MSG155, 'updated_guid': guid})

    return render(request, 'org_announcement.html', context)


@login_required
def update_org_announcement_details(request):
    update_user_info(request)
    if request.method == 'POST' and request.is_ajax():
        org_announcement_data = JsonParser().get_json_from_req(request)

        update_announcement_guid = org_announcement_data['announcement_guid']
        update_announcement_id = org_announcement_data['announcement_id']
        update_announcement_subject = org_announcement_data['announcement_subject']
        update_announcement_description = org_announcement_data['announcement_description']
        update_status = org_announcement_data['status']
        update_priority = org_announcement_data['priority']
        update_announcement_from_date = org_announcement_data['announcement_from_date']
        update_announcement_to_date = org_announcement_data['announcement_to_date']

        update_announcement_data = django_query_instance.django_filter_only_query(OrgAnnouncements, {
            'unique_announcement_id': update_announcement_guid,
            'del_ind': False})
        if org_announcement_data['del_ind']:
            OrgAnnouncements.objects.filter(unique_announcement_id=org_announcement_data['announcement_guid']).update(
                del_ind=True)
            message = MSG113
        else:
            update_announcement_data.update(
                announcement_subject=update_announcement_subject,
                announcement_id=update_announcement_id,
                announcement_description=update_announcement_description,
                status=update_status,
                priority=update_priority,
                announcement_from_date=update_announcement_from_date,
                announcement_to_date=update_announcement_to_date,
            )
            message = MSG156

    return JsonResponse({'message': message})




def org_support_save(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    obj_id = django_query_instance.django_get_query(OrgModel, {
        'object_id': global_variables.GLOBAL_LOGIN_USER_OBJ_ID, 'del_ind': False
    })

    username_values = []
    user_dropdown_values = django_query_instance.django_filter_only_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })
    for val in user_dropdown_values:
        username_values.append(val.username)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'username_values': username_values,
    }

    if request.method == "POST" and request.is_ajax():
        org_support_data = JsonParser().get_json_from_req(request)

        for data in org_support_data:
            guid = data['org_support_guid']
            if guid == '':
                guid = guid_generator()

            defaults = {
                'org_support_guid': guid,
                'org_support_types': data['support_type'],
                'org_support_email': data['support_email'],
                'org_support_number': data['support_number'],
                'username': data['username'],
                'client': client,
                'del_ind': False,
                'object_id': obj_id,
            }

            django_query_instance.django_update_or_create_query(OrgSupport, {'org_support_guid': guid},
                                                                defaults)

        return JsonResponse({'message': MSG157, 'updated_guid': guid})

    return render(request, 'org_support.html', context)


@login_required
def update_org_support_details(request):
    update_user_info(request)
    if request.method == 'POST' and request.is_ajax():
        org_support_data = JsonParser().get_json_from_req(request)

        org_support_guid = org_support_data['org_support_guid'],
        org_support_types = org_support_data['support_type'],
        org_support_email = org_support_data['support_email'],
        org_support_number = org_support_data['support_number'],
        username = org_support_data['username'],

        update_announcement_data = django_query_instance.django_filter_only_query(OrgSupport, {
            'org_support_guid': org_support_guid,
            'del_ind': False})

        OrgSupport.objects.filter(org_support_guid=org_support_data['org_support_guid']).update(
            org_support_types=org_support_types,
            org_support_email=org_support_email,
            org_support_number=org_support_number,
            username=username,

        )
        message = MSG156

    return JsonResponse({'message': message})


def org_support_config(request):
    username_values = []
    user_dropdown_values = django_query_instance.django_filter_only_query(UserData, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False
    })
    user_names = list()
    user_first_names = list()
    for names in user_dropdown_values:
        user_names = {'user_name': names.username, 'user_data': names.first_name + ' ' + names.last_name + ' - ' + names.email}
        user_first_names.append(user_names)
    print(user_first_names)

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'user_first_names': user_first_names,
    }

    return render(request, 'org_support_config.html', context)


def get_support_data(request):
    call_support_data_array = []
    call_support_guid_array = []
    email_support_data_array = []
    email_support_guid_array = []
    chat_support_data_array = []
    chat_support_guid_array = []

    call_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'Call'
    })

    for val in call_support_data:
        call_support_data_array.append(val.org_support_number)
        call_support_guid_array.append(val.org_support_guid)

    email_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'EMAIL'
    })
    for val in email_support_data:
        email_support_data_array.append(val.org_support_email)
        email_support_guid_array.append(val.org_support_guid)

    chat_support_data = django_query_instance.django_filter_only_query(OrgSupport, {
        'client': global_variables.GLOBAL_CLIENT, 'del_ind': False, 'org_support_types': 'CHAT'
    })
    for val in chat_support_data:
        chat_support_data_array.append(val.username)
        chat_support_guid_array.append(val.org_support_guid)
    # print(chat_support_data_array)

    return JsonResponse(
        {'call_support_data_array': call_support_data_array, 'call_support_guid_array': call_support_guid_array,
         'email_support_data_array': email_support_data_array, 'email_support_guid_array': email_support_guid_array,
         'chat_support_data_array': chat_support_data_array, 'chat_support_guid_array': chat_support_guid_array})
