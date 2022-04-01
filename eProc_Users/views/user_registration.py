"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_registration.py
Usage:
    Saves the data for new user registration
    register_page : Get the form and the data from UI which user has entered  and saves the data to DB,returning the user_register.html page.
Author:
    Soni Vydyula
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from eProc_Basic.Utilities.constants.constants import CONST_PWD
from eProc_Basic.Utilities.messages.messages import MSG017
from eProc_Registration.Utilities.registration_specific import RegFncts
from eProc_Registration.Registration_Forms.user_registration_form import RegForm

# Initializing message class from message.py
from eProc_Shopping_Cart.context_processors import update_user_info


@login_required
@transaction.atomic
def register_page(request):
    """
    :param request: Request data from UI
    :return: render user_register.html
    """
    update_user_info(request)
    reg_form = RegForm()
    if request.method == 'POST':
        reg_form = RegForm(request.POST or None)

        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            new_user.password = make_password(CONST_PWD)
            new_user.password2 = make_password(CONST_PWD)
            is_created = RegFncts.create_user(request, new_user)
            if is_created:
                messages.success(request, MSG017)
                return redirect('eProc_Users:register_page')

    context = {
        'inc_nav': True,
        'inc_footer': True,
        'reg_form': reg_form,
    }

    return render(request, 'User Registration/user_register.html', context)
