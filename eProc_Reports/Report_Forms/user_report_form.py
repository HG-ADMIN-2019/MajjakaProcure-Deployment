# The purpose of a form is to give users a chance to enter data and submit it to a server.
# Form for User Reports

# Importing the Django standard libraries
from django import forms
from django.utils.safestring import mark_safe
from datetime import date

from eProc_Configuration.models import OrgCompanies


class UserReportForm(forms.Form):
    # User report fields
    user_rep_types = (
        ('Users_in_company', 'Users in Company'),
        ('Substitute', 'Substitute'),
        ('Approval Hierarchy', 'Approval Hierarchy')
    )

    userrep_type = forms.ChoiceField(label='Select Report', choices=user_rep_types, required=False, disabled=True,
                                     widget=forms.Select(
                                         attrs={'class': 'form-control', "onchange": 'getSubReport(this.value)'}))

    # Users in Company search fields
    company_code = forms.ModelChoiceField(label='Company Code', required=False,
                                          queryset=OrgCompanies.objects.filter(del_ind=False), empty_label="Select",
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'}))

    active = forms.CharField(label='Active', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-control', 'style': 'width:20px; height:20px; margin-top:5px;'}))
    ####################################################

    ######## Substitutes in Company search fields ################################
    substitute_types = (
        ('Approval', 'Approval'),
        ('Goods_Receipt', 'Goods Receipt')
    )
    substitute_sub_type = forms.ChoiceField(label='Substitute Type', choices=substitute_types, required=False,
                                            widget=forms.Select(attrs={'class': 'hg_choiceField'}))

    ##############################################################

    def clean(self):
        cleaned_data = super(UserReportForm, self).clean()
