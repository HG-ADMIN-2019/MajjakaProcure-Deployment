"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_registration_form.py
Usage:
   User register form fields
    Regform : This class is used to build the form for user registration page.
Author:
    Soni Vydyula
"""
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import forms
from django.forms import ModelForm
from django import forms
import re

from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import *
from eProc_Registration.models import UserData


class RegForm(ModelForm):
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 required=True)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=False)
    phone_num = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=False)
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control'}), label='Language')
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control'}), label='Currency')
    time_zone = forms.ModelChoiceField(queryset=TimeZone.objects.all(), empty_label="None", widget=forms.Select(
        attrs={'class': 'form-control'}), label='TimeZone')
    email = forms.EmailField(label='E-mail', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Meta data for UserData model
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_num', 'employee_id', 'language_id',
                  'time_zone',
                  'date_format', 'decimal_notation', 'currency_id', 'user_type']

        DATE_FORMAT_CHOICES = (
            ('DD.MM.YYYY', 'DD.MM.YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('MM-DD-YYYY', 'MM-DD-YYYY'),
            ('YYYY.MM.DD', 'YYYY.MM.DD'),
            ('YYYY/MM/DD', 'YYYY/MM/DD'),
            ('YYYY-MM-DD', 'YYYY-MM-DD'))
        DECIMAL_NOTATION_CHOICES = (
            ('1.234.567,89', '1.234.567,89'),
            ('1,234,567.89', '1,234,567.89'),
            ('1 234 567,89', '1 234 567,89')
        )
        USER_TYPE = (
            ('Buyer', 'Buyer'),
            ('Supplier', 'Supplier'),
            ('Support', 'Support')
        )
        widgets = {
            'date_format': forms.Select(choices=DATE_FORMAT_CHOICES, attrs={'class': 'form-control'}),
            'decimal_notation': forms.Select(choices=DECIMAL_NOTATION_CHOICES,
                                             attrs={'class': 'form-control'}),
            'user_type': forms.Select(choices=USER_TYPE, attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_username(self):
        """
        # User name validation
        :return: username in uppercase
        """
        uname = self.cleaned_data.get('username')

        if not re.match('\w', uname):
            raise forms.ValidationError("Your username must contain at least four alphanumeric characters")
        elif not (uname.isalnum() and re.match('[A-Za-z0-9]{4,16}', uname)):
            raise forms.ValidationError("Must contain min four alphanumeric characters without special characters")
        elif UserData.objects.filter(username=uname, client=global_variables.GLOBAL_CLIENT).exists():
            raise forms.ValidationError('Username already exists')

        return uname.upper()

    def clean_first_name(self):
        """
        # First name validation
        :return: first name
        """
        fname = self.cleaned_data.get('first_name')
        if not (fname.isalpha() and re.match('[a-zA-Z]{4,30}', fname)):
            raise forms.ValidationError("Must contain min four characters without special characters/numbers")
        return fname.capitalize()

    def clean_last_name(self):
        """
        # Last name validation
        :return: lastname
        """
        lname = self.cleaned_data.get('last_name')
        if not (lname.isalpha() and re.match('[a-zA-Z]{1,30}', lname)):
            raise forms.ValidationError("Must contain min one character without special characters/numbers")
        return lname

    def clean_phone_num(self):
        """
        # Phone number validation
        :return: phone number
        """
        pnum = self.cleaned_data.get('phone_num')
        if not re.match('[0-9+()\-\ ]{10,30}', pnum) and len(pnum) > 0:
            raise forms.ValidationError("Must contain atleast 10 digits")
        return pnum

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserData.objects.filter(email=email, client=global_variables.GLOBAL_CLIENT).exists():
            raise forms.ValidationError("User email already exists")
        return email
