# Python functions that takes a web request and returns a web response
"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_login.py
Usage:
     login_page - Used to authenticate user to the application and locks the user from logging in after 3 unsuccessful login
     logout_page - This functionality allows a logged in user to logout of the application & redirects to login.html

Author:
    Babu / Siddarth / Sanjay
"""
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from eProc_Basic.Utilities.functions.get_db_query import *
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG029, MSG055, MSG056, MSG057, MSG122
from eProc_Login.Utilities.login_specific import UserFncts, login_attribute
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries

django_query_instance = DjangoQueries()


def login_page(request):
    """
        :param request:Takes email, password as input from user if login is True then redirects to Home Page
        :return: Login/login.html
    """
    attempts_left = ''

    if request.method == 'POST':
        email = request.POST.get('email-id')
        password = request.POST.get('password')

        if django_query_instance.django_existence_check(UserData, {'email': email}):
            user_details = django_query_instance.django_get_query(UserData, {
                'email': email
            })

            client = user_details.client_id
        else:
            messages.error(request, MSG055)
            return redirect('/')

        # Start of MEP:08-gets the login attempts for the client
        login_attempts = login_attribute(client)
        # Check if the password is locked, if locked display the message else allow the user to login

        if user_details.login_attempts == login_attempts and user_details.pwd_locked is True:
            messages.error(request, MSG056)

        else:
            login_user = UserFncts.login_user(request, email, password)
            if login_user is not None:
                global_variables.GLOBAL_SUB_MENU = {}
                global_variables.GLOBAL_SLIDE_MENU = {}
                global_variables.GLOBAL_CLIENT = getClients(request)
                global_variables.GLOBAL_LOGIN_USERNAME = getUsername(request)
                global_variables.GLOBAL_LOGIN_USER_EMAIL_ID = getUserEmailId(request)
                global_variables.GLOBAL_LOGIN_USER_OBJ_ID = get_login_obj_id(request)
                next_page = request.GET.get('next')

                if next_page is not None and next_page != '':
                    return HttpResponseRedirect(next_page)

                # checks for user first login or not
                first_login_check = request.user.date_joined
                if first_login_check is not None and first_login_check != '':
                    update_user_info(request)
                    update_user_roles_to_session(request)
                    django_query_instance.django_filter_only_query(UserData, {
                        'email': email, 'client': client, 'del_ind': False
                    }).update(login_attempts=0)
                    if request.user.is_superuser:
                        return HttpResponseRedirect('/org_model/org_structure/')
                    else:
                        return HttpResponseRedirect('/home')
                else:
                    # if request.user.is_superuser:
                        # update_initial_db_table(request.user.username, '700')
                    return HttpResponseRedirect('/password/')

            # If Login Credentials are invalid display error message and increase login_attempts by 1
            else:
                messages.error(request, MSG029)
                first_login_check = user_details.date_joined
                if user_details.login_attempts < int(login_attempts) and first_login_check is not None:
                    user_details.login_attempts = user_details.login_attempts + 1
                    user_details.save()
                    attempts = int(login_attempts) - user_details.login_attempts
                    attempts_left = str(attempts) + MSG057

                # If Number of login_attempts is 3 then pwd_locked will be True
                if 0 < int(login_attempts) == user_details.login_attempts:

                    # if user_details.login_attempts == int(login_attempts):
                    user_details.pwd_locked = True
                    user_details.save()
                    return redirect('eProc_Login:user_locked')
                else:
                    user_details.pwd_locked = False
                    user_details.save()

    return render(request, 'Login/login.html', {'attempts_left': attempts_left})


# user logout function
def logout_page(request):
    """
    :param request: On click of sign out, logs out user from session
    :return: After successfully logging out redirects to login Page
    """
    UserFncts.logout_user(request)
    if request.user.is_authenticated:
        return HttpResponse('Failed')
    else:
        return HttpResponseRedirect('/')


def user_lock(request):
    """
    :param request: Takes request as parameter
    :return: returns Userlocking.html in response
    """
    return render(request, 'User_Locking/Userlocking.html')


# To be removed after password unlock functionality is developed
def unlock_user(request):
    locked_users = django_query_instance.django_filter_only_query(UserData, {'login_attempts': 3, 'pwd_locked': True})
    locked_users.update(login_attempts=0, pwd_locked=False)
    return HttpResponseRedirect('/')
