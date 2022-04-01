"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    supplier_registration_form.py
Usage:
    Supplier register form fields
    SupplierRegForm : This class is used to build the form for supplier registration page.
Author:
    Siddarth Menon
"""

from django import forms
import re
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import Currency, Languages, Country, SupplierMaster
import datetime


class SupplierRegForm(forms.Form):
    supplier_id = forms.CharField(label='Supplier id', required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    supplier_types = (
        ('E-mail Supplier', 'E-mail Supplier'),
        ('Mail Supplier', 'Mail Supplier'),
        ('Integrated Supplier', 'Integrated Supplier'),
    )
    supp_type = forms.CharField(label='Communication Type', required=True,
                                widget=forms.Select(choices=supplier_types, attrs={'class': 'form-control'}))
    name1 = forms.CharField(label='Name 1', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name2 = forms.CharField(label='Name 2', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email1 = forms.EmailField(label='E-mail 1', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email2 = forms.EmailField(label='E-mail 2', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email3 = forms.EmailField(label='E-mail 3', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email4 = forms.EmailField(label='E-mail 4', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email5 = forms.EmailField(label='E-mail 5', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    landline = forms.CharField(label='Landline', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_num = forms.CharField(label='Mobile', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    fax = forms.CharField(label='Fax', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(label='Street', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(label='Postal code', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label='City', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_code = forms.ModelChoiceField(queryset=Country.objects.all(), label='Country',
                                          empty_label=" Please select country from drop-down ", required=True,
                                          widget=forms.Select(
                                              attrs={'class': 'form-control'}))
    language_id = forms.ModelChoiceField(queryset=Languages.objects.all(), required=True, label='Language',
                                         empty_label=" Please select language from drop-down ", widget=forms.Select(
            attrs={'class': 'form-control'}))
    currency_id = forms.ModelChoiceField(queryset=Currency.objects.all(), required=True, label='Currency',
                                         empty_label=" Please select currency in drop-down ", widget=forms.Select(
            attrs={'class': 'form-control'}))
    registration_number = forms.CharField(label='Registration number', required=True,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_term1 = forms.CharField(label='Search Term 1', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_term2 = forms.CharField(label='Search Term 2', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    working_days = forms.CharField(label='Working Days', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    duns_number = forms.CharField(label='Duns Number', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    lockdate = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'min': datetime.date.today(), 'max': '9999-12-12'}),
        label='Lock Date',
        required=False,
    )
    output_medium_types = (
        ('Print', 'Print'),
        ('Mail', 'Mail'),
        ('Fax', 'Fax'),
        ('XML / XI', 'XML / XI'),
    )
    output_medium = forms.CharField(widget=forms.Select(choices=output_medium_types, attrs={'class': 'form-control'}))
    supplier_image = forms.FileField(label='sample photo', widget=forms.FileInput, required=False)

    def clean_name1(self):
        """
        # Name 1 validation
        :return: first name
        """
        name1 = self.cleaned_data.get('name1')
        if not (name1.isalpha() and re.match('[a-zA-Z]{4,30}', name1)):
            raise forms.ValidationError(MSG079)
        return name1

    def clean_name2(self):
        """
        # Name 2 validation
        :return: second name
        """
        lname = self.cleaned_data.get('name2')
        if not (lname.isalpha() and re.match('[a-zA-Z]{1,30}', lname)):
            raise forms.ValidationError(MSG080)
        return lname

    def clean_mobile_num(self):
        """
        # Mobile number validation
        :return: mobile phone number
        """
        mnum = self.cleaned_data.get('mobile_num')
        if not re.match('[0-9+()\-\ ]{10,30}', mnum) and len(mnum) > 0:
            raise forms.ValidationError(MSG077)
        else:
            return mnum

    def clean_supplier_id(self):
        supp_id = self.cleaned_data.get('supplier_id')
        if SupplierMaster.objects.filter(supplier_id=supp_id, client=global_variables.GLOBAL_CLIENT).exists():
            raise forms.ValidationError(MSG085)
        return supp_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check = SupplierMaster.objects.filter(email=email, client=global_variables.GLOBAL_CLIENT).exists()
        if check:
            raise forms.ValidationError(MSG083)
        else:
            return email

    def clean_registration_number(self):
        reg_number = self.cleaned_data.get('registration_number')
        if SupplierMaster.objects.filter(registration_number=reg_number).exists():
            raise forms.ValidationError('Supplier Registration number already exists')
        return reg_number
