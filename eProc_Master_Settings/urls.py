from django.urls import path
from . import views

app_name = 'eProc_Master_Settings'

urlpatterns = [
    path('data_upload_fk/', views.data_upload_fk, name='data_upload_fk'),
    path('render_aav_data/', views.render_aav_data, name='render_aav_data'),
    path('extract_aav_data/', views.extract_aav_data, name='extract_aav_data'),
    path('extract_accdesc_data/', views.extract_accdesc_data, name='extract_accdesc_data'),
    path('extract_cusprodcat_data', views.extract_cusprodcat_data, name='extract_cusprodcat_data'),
    path('extract_cusprodcat_template', views.extract_cusprodcat_template, name='extract_cusprodcat_template'),
    path('extract_cusprodcatdesc_data', views.extract_cusprodcatdesc_data, name='extract_cusprodcatdesc_data'),
    path('extract_cusprodcatdesc_template', views.extract_cusprodcatdesc_template, name='extract_cusprodcatdesc_template'),
    path('extract_workflowschema_data', views.extract_workflowschema_data, name='extract_workflowschema_data'),
    path('extract_workflowacct_template', views.extract_workflowacct_template, name='extract_workflowacct_template'),
    path('extract_workflowschema_template', views.extract_workflowschema_template, name='extract_workflowschema_template'),
    path('extract_workflowaccount_data', views.extract_workflowaccount_data, name='extract_workflowaccount_data'),
    path('ACC_values', views.account_ass_values, name='account_ass_values'),
    path('save_master_settings_data', views.save_master_settings_data, name='save_master_settings_data'),
    path('save_product_cat_cust', views.save_product_cat_cust, name='save_product_cat_cust'),
    path('get_prod_cat_image_detail', views.get_prod_cat_image_detail, name='get_prod_cat_image_detail'),
    path('upload_prod_cat_images', views.upload_prod_cat_images, name='upload_prod_cat_images'),
    path('check_data_acct_asst_val', views.check_data_acct_asst_val, name='check_data_acct_asst_val'),
    path('INCO_terms', views.display_incoterms, name='display_incoterms'),
    path('payment_terms', views.payment_terms, name='payment_terms'),
    path('companies', views.org_companies, name='org_companies'),
    path('approval_types', views.approval_type, name='approval_type'),
    path('work_flow_schemas', views.work_flow_schema, name='work_flow_schema'),
    path('spending_limit_values', views.spend_limit_value, name='spend_limit_value'),
    path('general_ledger_accounts', views.det_gl_acc, name='det_gl_acc'),
    path('ACC_value_descriptions', views.account_assignment, name='account_assignment'),
    path('purchasing_organizations', views.purchasing_org, name='purchasing_org'),
    path('purchasing_groups', views.purchasing_grp, name='purchasing_grp'),
    path('payment_term_descriptions', views.payment_terms_desc, name='payment_terms_desc'),
    path('approver_limits', views.approval_limit, name='approval_limit'),
    path('approver_limit_values', views.approval_limit_value, name='approval_limit_value'),
    path('spending_limits', views.spend_limit_id, name='spend_limit_id'),
    path('workflows', views.work_flow_accounting, name='work_flow_accounting'),
    path('upload_supplier', views.upload_supplier, name='upload_supplier'),
    path('upload', views.upload, name='upload'),
    path('address_types', views.address_type, name='address_type'),
    path('addresses', views.address, name='address'),
    path('extract_approverlimit_data/', views.extract_approverlimit_data, name='extract_approverlimit_data'),
    path('extract_approverlimitval_data/', views.extract_approverlimitval_data, name='extract_approverlimitval_data'),
    path('extract_spendlimit_data/', views.extract_spendlimit_data, name='extract_spendlimit_data'),
    path('extract_spendlimit_template/', views.extract_spendlimit_template, name='extract_spendlimit_template'),
    path('extract_spendlimitval_data/', views.extract_spendlimitval_data, name='extract_spendlimitval_data'),
    path('extract_orgcompany_data/', views.extract_orgcompany_data, name='extract_orgcompany_data'),
    path('create_update_master_data', views.create_update_master_data, name='create_update_master_data'),
    path('extract_address_type_data', views.extract_address_type_data, name='extract_address_type_data'),
    path('extract_address_type_template', views.extract_address_type_template, name='extract_address_type_template'),
    path('extract_glaccount_data', views.extract_glaccount_data, name='extract_glaccount_data'),
    path('extract_glaccount_template', views.extract_glaccount_template, name='extract_glaccount_template'),
    path('extract_pgrp_data', views.extract_pgrp_data, name='extract_pgrp_data'),
    path('extract_pgrp_template', views.extract_pgrp_template, name='extract_pgrp_template'),
    path('extract_porg_data', views.extract_porg_data, name='extract_porg_data'),
    path('extract_porg_template', views.extract_porg_template, name='extract_porg_template'),
    path('extract_address_data', views.extract_address_data, name='extract_address_data'),
    path('extract_approvertype_template', views.extract_approvertype_template, name='extract_approvertype_template'),
    path('extract_approver_type_data', views.extract_approver_type_data, name='extract_approver_type_data'),
    path('extract_incoterms_data', views.extract_incoterms_data, name='extract_incoterms_data'),
    path('extract_incoterm_template', views.extract_incoterm_template, name='extract_incoterm_template'),
    path('extract_payterms_data', views.extract_payterms_data, name='extract_payterms_data'),
    path('extract_payterm_template', views.extract_payterm_template, name='extract_payterm_template'),
    path('custom_UNSPSC_codes', views.upload_cust_prod_cat, name='upload_cust_prod_cat'),
    path('custom_UNSPSC_code_descriptions', views.upload_cust_prod_cat_desc, name='upload_cust_prod_cat_desc'),
    path('extract_spendlimitval_data_template', views.extract_spendlimitval_data_template, name='extract_spendlimitval_data_template'),
    path('extract_accdesc_data_template', views.extract_accdesc_data_template, name='extract_accdesc_data_template'),
    path('extract_aav_data_template', views.extract_aav_data_template, name='extract_aav_data_template'),
    path('extract_address_data_Template', views.extract_address_data_Template, name='extract_address_data_Template'),
    path('extract_approverlimit_data_template', views.extract_approverlimit_data_template, name='extract_approverlimit_data_template'),
    path('extract_approverlimitval_data_template', views.extract_approverlimitval_data_template,name='extract_approverlimitval_data_template'),
    path('extract_orgcompany_data_template', views.extract_orgcompany_data_template,name='extract_orgcompany_data_template'),

]
