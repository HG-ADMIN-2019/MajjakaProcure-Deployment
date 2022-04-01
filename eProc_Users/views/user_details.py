"""Copyright (c) 2020 Hiranya Garbha, Inc.
    Name:
        user_details.py
    Usage:
        Story SP12-10
        Function to get the user details
        Taking the user email id and getting details and rendering back to the user details page

     Author:
        Varsha Prasad
"""

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Basic.Utilities.constants.constants import CONST_DECIMAL_NOTATION, CONST_DATE_FORMAT
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.messages.messages import MSG183
from eProc_Configuration.models import *
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import convert_to_boolean
from eProc_Shopping_Cart.context_processors import update_user_info

django_query_instance = DjangoQueries()





@login_required()
@transaction.atomic
def update_user_basic_details(request):
    if request.method == 'POST':
        update_user_basic_data = django_query_instance.django_filter_only_query(UserData,
                                                                                {'email': request.POST.get('email'),
                                                                                 'del_ind': False})

        update_user_basic_data.update(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone_num=request.POST.get('phone_num'),
            language_id=request.POST.get('language_id'),
            time_zone=request.POST.get('time_zone'),
            date_format=request.POST.get('date_format'),
            employee_id=request.POST.get('employee_id'),
            decimal_notation=request.POST.get('decimal_notation'),
            currency_id=request.POST.get('currency_id'),
            user_type=request.POST.get('user_type'),
            user_locked=convert_to_boolean(request.POST.get('user_locked')),
            pwd_locked=convert_to_boolean(request.POST.get('pwd_locked')),
            is_superuser=convert_to_boolean(request.POST.get('super_user')),
        )
        return JsonResponse({'message': MSG183})
