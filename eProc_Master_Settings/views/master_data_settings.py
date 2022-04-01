import json
from itertools import chain

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.get_db_query import get_country_data
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.update_del_ind import query_update_del_ind
from eProc_Basic.Utilities.functions.update_del_ind import update_del_ind
from eProc_Basic_Settings.Utilities.basic_settings_specific import *
from eProc_Catalog.Utilities.catalog_specific import save_prod_cat_cust_image_to_db
from eProc_Catalog.views import json_obj
from eProc_Master_Settings.Utilities.master_settings_specific import *
from eProc_Configuration.models.development_data import AccountAssignmentCategory
from eProc_Master_Settings.Utilities.master_settings_specific import *
from eProc_Master_Settings.Utilities.master_settings_specific import save_master_data_into_db, save_aav_data_into_db, \
    save_aad_data_into_db, save_app_limit_data_into_db, save_app_limit_value_data_into_db
from eProc_Master_Settings.Utilities.master_settings_specific import save_spend_limit_data_into_db, \
    save_address_type_data_into_db, save_glaccount_data_into_db, save_purorg_data_into_db, save_purgrp_data_into_db, \
    save_spend_limit_value_data_into_db, save_payterm_data_into_db, save_address_data_into_db, \
    save_product_cat_cust_data_into_db
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_basic_pk_fk_tables import UploadPkFkTables
from eProc_Upload.Utilities.upload_data.upload_pk_tables import *
from eProc_Upload.Utilities.upload_specific.upload_suppliers import upload_suppliermaster_new

JsonParser_obj = JsonParser()

upload_data_response = ''


def create_update_master_data(request):
    update_user_info(request)
    master_data = JsonParser_obj.get_json_from_req(request)
    if master_data['table_name'] == 'UnspscCategoriesCust':
        display_data = save_product_cat_cust_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'UnspscCategoriesCustDesc':
        display_data = save_product_cat_cust_desc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'WorkflowSchema':
        display_data = save_work_flow_schema_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'SpendLimitId':
        display_data = save_spend_limit_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgAddressMap':
        display_data = save_address_type_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'DetermineGLAccount':
        display_data = save_glaccount_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'AccountingData':
        display_data = save_aav_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverLimit':
        display_data = save_app_limit_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverLimitValue':
        display_data = save_app_limit_value_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'SpendLimitValue':
        display_data = save_spend_limit_value_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Payterms':
        display_data = save_payterm_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgAddress':
        display_data = save_address_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'ApproverType':
        display_data = save_approval_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'WorkflowACC':
        display_data = save_workflow_acc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Incoterms':
        display_data = save_incoterms_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'Payterms_desc':
        display_data = save_payment_desc_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgPGroup':
        display_data = save_purgrp_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgPorg':
        display_data = save_purorg_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'AccountingDataDesc':
        display_data = save_aad_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgCompanies':
        display_data = save_company_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'UserRoles':
        display_data = save_roles_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgNodeTypes':
        display_data = save_orgnode_types_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'OrgAttributes':
        display_data = save_orgattributes_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)
    if master_data['table_name'] == 'AuthorizationObject':
        display_data = save_authorobject_data_into_db(master_data)
        return JsonResponse(display_data, safe=False)


def save_master_settings_data(request):
    """

    :param request:
    :return:
    """

    client = getClients(request)
    basic_data = JsonParser_obj.get_json_from_req(request)
    Table_nam = basic_data['Dbl_clck_tbl_id']
    del basic_data['Dbl_clck_tbl_id']

    basic_data_list = []

    for value in basic_data.values():
        basic_data_list.append(value)

    # FunctionResponse  = save_master_data_into_db ( basic_data_list,Table_name,client )
    upload_data_response = save_master_data_into_db(basic_data_list, Table_nam, client)
    return JsonResponse(upload_data_response, safe=False)

    Table_name = ''
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id', 'description'))
    upload_data_company = list(
        OrgCompanies.objects.filter(del_ind=False).values('company_guid', 'object_id', 'name1', 'name2', 'company_id'))
    upload_data_acccat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat', 'description'))
    upload_data_accounting = list(
        AccountingData.objects.filter(del_ind=False).values('account_assign_guid', 'account_assign_value', 'valid_from',
                                                            'valid_to', 'account_assign_cat', 'company_id'))
    upload_data_acc_desc = list(
        AccountingDataDesc.objects.filter(del_ind=False).values('acc_desc_guid', 'account_assign_value', 'description',
                                                                'account_assign_cat', 'company_id', 'language_id'))
    upload_data_language = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    upload_data_apptypes = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))
    upload_data_app_lim = list(
        ApproverLimit.objects.filter(del_ind=False).values('app_guid', 'approver_username', 'app_code_id',
                                                           'company_id'))
    upload_data_app_lim_val = list(
        ApproverLimitValue.objects.filter(del_ind=False).values('app_lim_dec_guid', 'app_types', 'app_code_id',
                                                                'currency_id', 'upper_limit_value', 'company_id'))
    ###########
    upload_data_cust_prod_cat = list(
        UnspscCategoriesCust.objects.filter(client=client, del_ind=False).values('prod_cat_guid', 'prod_cat_id'))
    ###########
    upload_data_spnd_lim_id = SpendLimitId.objects.filter(client=client, del_ind=False)
    upload_data_spnd_lim_val = SpendLimitValue.objects.filter(client=client, del_ind=False)
    upload_data_wfschema = WorkflowSchema.objects.filter(client=client, del_ind=False)
    upload_data_wfacc = WorkflowACC.objects.filter(client=client, del_ind=False)
    upload_data_OrgPorg = OrgPorg.objects.filter(client=client, del_ind=False)
    upload_data_OrgPGroup = OrgPGroup.objects.filter(client=client, del_ind=False)
    upload_data_Orgmodel = OrgModel.objects.filter(client=client, del_ind=False)
    upload_data_OrgCompanies = OrgCompanies.objects.filter(client=client, del_ind=False)
    upload_data_UserRoles = UserRoles.objects.filter(del_ind=False)
    upload_data_AuthorizationObject = AuthorizationObject.objects.filter(del_ind=False)
    upload_data_AuthorizationGroup = AuthorizationGroup.objects.filter(del_ind=False)
    upload_data_Authorization = Authorization.objects.filter(client=client, del_ind=False)

    if Table_name == 'upload_accdata':
        Upload_response = list(chain(upload_data_accounting, upload_data_acccat, upload_data_company))

        accassval_data = {}
        accassval_data['accassval'] = list(Upload_response)
        return JsonResponse(accassval_data)

    elif Table_name == 'upload_accdatades':
        Upload_response = list(
            chain(upload_data_acc_desc, upload_data_acccat, upload_data_language, upload_data_company))
    elif Table_name == 'upload_apptypes':
        Upload_response = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))
    elif Table_name == 'upload_applimit':
        Upload_response = list(chain(upload_data_app_lim, upload_data_company))
    elif Table_name == 'upload_applimval':
        Upload_response = list(
            chain(upload_data_app_lim_val, upload_data_apptypes, upload_data_company, upload_data_currency))
    elif Table_name == 'upload_spndlimid':
        Upload_response = list(chain(upload_data_spnd_lim_id, upload_data_company))
    #############
    elif Table_name == 'upload_custprodcat':
        Upload_response = list(upload_data_cust_prod_cat)
        prodcatcust_data = {}
        prodcatcust_data['prod_cat_cust'] = list(Upload_response)
        return JsonResponse(prodcatcust_data)

    elif Table_name == 'upload_wfschema':
        Upload_response = list(upload_data_work_flow_schema)
        workflowschema_data = {}
        workflowschema_data['work_flow_schema'] = list(Upload_response)
        return JsonResponse(workflowschema_data)

    elif Table_name == 'upload_WFACC':
        Upload_response = list(upload_data_work_flow_schema)
        workflowaccounting_data = {}
        workflowaccounting_data['work_flow_accounting'] = list(Upload_response)
        return JsonResponse(workflowaccounting_data)
    #############
    elif Table_name == 'upload_spndlimval':
        Upload_response = list(chain(upload_data_spnd_lim_val, upload_data_company, upload_data_currency))
    elif Table_name == 'upload_WFACC':
        Upload_response = list(chain(upload_data_wfacc, upload_data_acccat, upload_data_currency, upload_data_company))
    elif Table_name == 'upload_orgnodetypes':
        Upload_response = OrgNodeTypes.objects.filter(client=client, del_ind=False)
    elif Table_name == 'upload_orgattributes':
        Upload_response = OrgAttributes.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_companies':
        Upload_response = list(chain(upload_data_OrgCompanies, upload_data_Orgmodel))
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_porg':
        Upload_response = list(chain(upload_data_OrgPorg, upload_data_Orgmodel, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_pgrp':
        Upload_response = list(chain(upload_data_OrgPGroup, upload_data_OrgPorg, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_roles':
        Upload_response = UserRoles.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_authobj':
        Upload_response = AuthorizationObject.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_authgrp':
        Upload_response = list(chain(upload_data_AuthorizationGroup, upload_data_AuthorizationObject))
        return JsonParser_obj.get_json_from_obj(Upload_response)
    elif Table_name == 'upload_auth':
        Upload_response = list(chain(upload_data_Authorization, upload_data_UserRoles))
        return JsonParser_obj.get_json_from_obj(Upload_response)

    # if not upload_data_response[0]:
    #     return JsonResponse({'errmsg': upload_data_response[1]}, status=400)
    # else:
    # return JsonResponse({'successmsg': upload_data_response[1]})
    # return JsonParser_obj.get_json_from_obj(Upload_response)
    # display_data = {}
    # display_data['dataval'] = list(Upload_response)
    # print(display_data)
    # return JsonResponse(display_data)


def account_ass_values(request):
    client = getClients(request)
    upload_data_company = list(
        OrgCompanies.objects.filter(del_ind=False).values('company_id'))
    # upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_acccat = list(
        AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    upload_data_accounting = list(
        AccountingData.objects.filter(del_ind=False).values('account_assign_guid', 'account_assign_value', 'valid_from',
                                                            'valid_to', 'account_assign_cat', 'company_id'))

    Upload_response = list(upload_data_accounting)

    rendered_account_assignment_data = []

    for data in upload_data_accounting:
        data_dict = {
            'account_assign_guid': data['account_assign_guid'],
            'account_assign_value': data['account_assign_value'],
            'valid_from': data['valid_from'].strftime("%Y-%m-%d"),
            'valid_to': data['valid_to'].strftime("%Y-%m-%d"),
            'account_assign_cat': data['account_assign_cat'],
            'company_id': data['company_id']
        }
        rendered_account_assignment_data.append(data_dict)

    accassval_data = {}
    accassval_data['accassval'] = list(Upload_response)
    return render(request, 'Accounting_Data/account_assignment_values.html',
                  {'upload_account_assignment_value': Upload_response, 'upload_company_data': upload_data_company,
                   'upload_data_acccat': upload_data_acccat,
                   'rendered_account_assignment_data': rendered_account_assignment_data,
                   'inc_nav': True})


def render_aav_data(request):
    if request.method == 'POST':
        upload_data_accounting = list(
            AccountingData.objects.filter(del_ind=False).values('account_assign_guid', 'account_assign_value',
                                                                'valid_from',
                                                                'valid_to', 'account_assign_cat', 'company_id'))

        print(upload_data_accounting)

    return JsonResponse(upload_data_accounting, safe=False)


def extract_aav_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ACCOUNT ASSIGNMENT VALUES.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ACC_ASSIGN_VALUE', 'VAILD_FROM', 'VAILD_TO', 'ACCOUNT_ASSIGN_CAT', 'COMPANY_ID', 'del_ind'])

    accounting = django_query_instance.django_filter_query(AccountingData,
                                                           {'del_ind': False}, None,
                                                           ['account_assign_value', 'valid_from', 'valid_to',
                                                            'account_assign_cat', 'company_id', 'del_ind'])
    accounting_data = query_update_del_ind(accounting)

    for accountingData in accounting_data:
        accountingData_info = [accountingData['account_assign_value'], accountingData['valid_from'],
                               accountingData['valid_to'], accountingData['account_assign_cat'],
                               accountingData['company_id'], accountingData['del_ind']]
        writer.writerow(accountingData_info)

    return response


def extract_accdesc_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ACCOUNT ASSIGNMENT DESCRIPTION.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['ACCOUNT_ASSIGN_VALUE', 'DESCRIPTION', 'COMPANY_ID', 'LANGUAGE_ID', 'ACCOUNT_ASSIGN_CAT', 'del_ind'])

    accountingdesc = django_query_instance.django_filter_query(AccountingDataDesc,
                                                               {'del_ind': False}, None,
                                                               ['account_assign_value', 'description', 'company_id',
                                                                'language_id', 'account_assign_cat', 'del_ind'])
    accountingdesc_data = query_update_del_ind(accountingdesc)

    for accountingdescData in accountingdesc_data:
        accountingdescData_info = [accountingdescData['account_assign_value'], accountingdescData['description'],
                                   accountingdescData['company_id'], accountingdescData['language_id'],
                                   accountingdescData['account_assign_cat'], accountingdescData['del_ind']]
        writer.writerow(accountingdescData_info)

    return response


def extract_cusprodcat_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer_Product_Category.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PRODUCT CATEGORY ID', 'del_ind'])

    customerprod = django_query_instance.django_filter_query(UnspscCategoriesCust,
                                                             {'del_ind': False}, None,
                                                             ['prod_cat_id', 'del_ind'])

    customerprod_data = query_update_del_ind(customerprod)

    for customerprodData in customerprod_data:
        customerprodData_info = [customerprodData['prod_cat_id'],
                                 customerprodData['del_ind']]
        writer.writerow(customerprodData_info)

    return response



def extract_cusprodcat_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer_Product_Category_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PRODUCT CATEGORY ID', 'del_ind'])

    return response



def extract_cusprodcatdesc_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer_Product_Category_Description.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PRODUCT CATEGORY', 'CATEGORY_DESC', 'LANGUAGE_ID', 'del_ind'])
    # get only active record

    customerproddesc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                                 {'del_ind': False}, None,
                                                                 ['prod_cat_id', 'category_desc', 'language_id',
                                                                  'del_ind'
                                                                  ])
    customerproddesc_data = query_update_del_ind(customerproddesc)

    for customerproddescData in customerproddesc_data:
        customerproddescData_info = [customerproddescData['prod_cat_id'],
                                     customerproddescData['category_desc'],
                                     customerproddescData['language_id'],
                                     customerproddescData['del_ind']]
        writer.writerow(customerproddescData_info)

    return response



def extract_cusprodcatdesc_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Customer_Product_Category_Description_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PRODUCT CATEGORY', 'CATEGORY_DESC', 'LANGUAGE_ID', 'del_ind'])

    return response



def extract_workflowschema_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Work_Flow_Schema.CSV"'

    writer = csv.writer(response)

    writer.writerow(['WORKFLOW_SCHEMA', 'APP_TYPES', 'COMPANY_ID', 'del_ind'])

    workflowschema = django_query_instance.django_filter_query(WorkflowSchema,
                                                               {'del_ind': False}, None,
                                                               ['workflow_schema', 'app_types', 'company_id',
                                                                'del_ind'])

    workflowschema_data = query_update_del_ind(workflowschema)

    for workflowschemaData in workflowschema_data:
        workflowschema_info = [workflowschemaData['workflow_schema'],
                               workflowschemaData['app_types'],
                               workflowschemaData['company_id'],
                               workflowschemaData['del_ind']]
        writer.writerow(workflowschema_info)

    return response


def extract_workflowschema_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Work_Flow_Schema_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['WORKFLOW_SCHEMA', 'APP_TYPES', 'COMPANY_ID', 'del_ind'])

    return response


def extract_workflowaccount_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="WORK FLOW ACCOUNTING.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ACC_VALUE', 'COMPANY_ID', 'APP_USERNAME', 'SUP_COMPANY_ID', 'SUP_ACC_VALUE',
                     'WORKFLOW_ACC_SOURCE_SYSTEM', 'ACCOUNT_ASSIGN_CAT', 'CURRENCY_ID',
                     'SUP_ACCOUNT_ASSIGN_CAT', 'del_ind'])

    # get only active records
    workflow_acct = django_query_instance.django_filter_query(WorkflowACC,
                                                              {'del_ind': False}, None,
                                                              ['acc_value', 'company_id', 'app_username',
                                                               'sup_company_id',
                                                               'sup_acc_value', 'workflow_acc_source_system',
                                                               'account_assign_cat',
                                                               'currency_id', 'sup_account_assign_cat',
                                                               'del_ind'])
    workflow_acct_data = query_update_del_ind(workflow_acct)

    for workflowacct in workflow_acct_data:
        workflowacct_info = [workflowacct['acc_value'], workflowacct['company_id'], workflowacct['app_username'],
                             workflowacct['sup_company_id'], workflowacct['sup_acc_value'],
                             workflowacct['workflow_acc_source_system'], workflowacct['account_assign_cat'],
                             workflowacct['currency_id'],
                             workflowacct['sup_account_assign_cat'],
                             workflowacct['del_ind']]
        writer.writerow(workflowacct_info)

    return response


def save_product_cat_cust(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    product_not_exist = ''
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    product_data = json.loads(request.POST['update'])
    # save images
    if checkKey(converted_dict, 'Prod_cat'):
        prod_cat = converted_dict['Prod_cat']
        file_name = converted_dict['file_name']
        default_image = [True if img_flag else False for img_flag in converted_dict['default_image_value']]
        save_prod_cat_cust_image_to_db(prod_cat, file_name, attached_file, default_image)

    cust_prod_cat_not_exist: object = UnspscCategoriesCust.objects.filter(del_ind=False).exclude \
        (prod_cat_guid__in=[custprodcat['prod_cat_guid'] for custprodcat in product_data])

    for set_del_int in cust_prod_cat_not_exist:
        set_del_int.del_ind = True
        set_del_int.save()

    for save_custprodcat in product_data:
        product_category_id = save_custprodcat['prod_cat_id']

        # Below logic is for existing records changed.

        # Check if there is any change in the record if no then skip the record
        if (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                prod_cat_id=product_category_id,
                                                client=global_variables.GLOBAL_CLIENT).exists()):
            continue

        elif not (UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                      prod_cat_id=product_category_id,
                                                      client=global_variables.GLOBAL_CLIENT).exists()):

            if (UnspscCategoriesCust.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                    prod_cat_guid=save_custprodcat['prod_cat_guid'], ).exists()):
                UnspscCategoriesCust.objects.filter(prod_cat_guid=save_custprodcat['prod_cat_guid'],
                                                    client=global_variables.GLOBAL_CLIENT).update(
                    prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                    del_ind=False,
                    client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT))

        # Below logic is for new records added. The GUID will be hardcoded to GUID from UI and sent to backend.
        if save_custprodcat['prod_cat_guid'] == '':
            UnspscCategoriesCust.objects.create(
                prod_cat_guid=guid_generator(),
                prod_cat_id=UnspscCategories.objects.get(prod_cat_id=product_category_id),
                del_ind=False,
                client=OrgClients.objects.get(client=global_variables.GLOBAL_CLIENT))
    catalog_data_response = list(
        UnspscCategoriesCust.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values(
            'prod_cat_guid', 'prod_cat_id'))
    return JsonResponse(catalog_data_response, safe=False)


def get_prod_cat_image_detail(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    prod_cat_id = json_obj.get_json_from_req(request)
    prod_cat_img_detail = ImagesUpload.objects.filter(client=global_variables.GLOBAL_CLIENT,
                                                      image_id=str(prod_cat_id),
                                                      image_type=CONST_UNSPSC_IMAGE_TYPE)

    return json_obj.get_json_from_obj(prod_cat_img_detail)


def data_upload_fk(request):
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('utf8')
    # fin_upload_data = io.StringIO(data_set_val)
    upload_csv = CompareTableHeader()
    # upload_csv.header_data = fin_upload_data
    upload_csv.app_name = request.POST.get('appname')
    upload_csv.table_name = request.POST.get('Tablename')
    upload_csv.request = request
    basic_save, header_detail = upload_csv.basic_header_condition()
    # if not basic_save:
    try:

        # retrieving correct ordered data from csv_data_arrangement() - basic_settings_specific.py
        correct_order_list = csv_data_arrangement(db_header, data_set_val)

        return JsonResponse(correct_order_list, safe=False)

    except MultiValueDictKeyError:
        csv_file = False
        messages.error(request, MSG048)

    else:
        return JsonResponse(basic_save, safe=False)


def check_data_acct_asst_val(request):
    if request.is_ajax():
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        db_header_data = table_data__array['db_header_data']
        client = getClients(request)
        check_data_class = UploadPkFkTables()
        check_data_class.app_name = table_data__array['appname']
        check_data_class.table_name = table_data__array['Tablename']
        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = check_data_class.upload_master_data_new(popup_data_list, db_header_data, client)
        # print(check_variable)
        return JsonResponse(check_variable)

    return render(request, 'Accounting_Data/account_assignment_values.html')


def display_incoterms(request):
    incoterms_data = get_configuration_data(
        Incoterms, {'del_ind': False}, ['incoterm_key', 'description'])
    # incoterms_data = list(
    #     Incoterms.objects.filter(del_ind=False).values('incoterm_key', 'description'))
    dropdown_db_values = list(
        FieldTypeDesc.objects.filter(field_name='incoterm', del_ind=False).values('field_type_id',
                                                                                  'field_type_desc'
                                                                                  ))
    return render(request, 'Supplier_Management/incoterms.html',
                  {'incoterms_data': incoterms_data, 'dropdown_db_values': dropdown_db_values,
                   'inc_nav': True})


def payment_terms(request):
    payment_term_data = list(
        Payterms.objects.filter(del_ind=False).values('payment_term_key', 'payment_term_guid'))
    return render(request, 'Supplier_Management/payment_terms.html',
                  {'payment_term_data': payment_term_data,
                   'inc_nav': True})


def payment_terms_desc(request):
    client = getClients(request)
    payterm_key_list = list(Payterms.objects.filter(del_ind=False).values('payment_term_key'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    # payment_desc_data = list(
    #     Payterms_desc.objects.filter(del_ind=False).values('payment_term_guid', 'payment_term_key', 'day_limit',
    #                                                         'description', 'language_id'))
    payment_desc_data = get_configuration_data(
        Payterms_desc, {'client': client, 'del_ind': False}, ['payment_term_guid', 'payment_term_key', 'day_limit',
                                                              'description', 'language_id'])
    return render(request, 'Supplier_Management/payment_term_desc.html',
                  {'payment_desc_data': payment_desc_data, 'payterm_key_list': payterm_key_list,
                   'language_list': language_list, 'inc_nav': True})


def upload_supplier(request):
    update_user_info(request)
    supplier_data = list(
        SupplierMaster.objects.filter(del_ind=False, client=global_variables.GLOBAL_CLIENT).values('supplier_id',
                                                                                                   'supp_type', 'name1',
                                                                                                   'name2', 'city',
                                                                                                   'postal_code',
                                                                                                   'street', 'landline',
                                                                                                   'mobile_num', 'fax',
                                                                                                   'email', 'email1',
                                                                                                   'email2', 'email3',
                                                                                                   'email4', 'email5',
                                                                                                   'output_medium',
                                                                                                   'search_term1',
                                                                                                   'search_term2',
                                                                                                   'duns_number',
                                                                                                   'block_date',
                                                                                                   'block',
                                                                                                   'working_days',
                                                                                                   'is_active',
                                                                                                   'registration_number',
                                                                                                   'country_code',
                                                                                                   'currency_id',
                                                                                                   'language_id'))
    return render(request, 'Supplier_Management/supplier_upload.html',
                  {'supplier_data': supplier_data, 'inc_nav': True,
                   'supplier_data_json': json.dumps(supplier_data, cls=DjangoJSONEncoder)})


def upload(request):
    if request.is_ajax():
        Test_mode = 'on'
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        # db_header_data = table_data__array['db_header_data']
        # check_data_class = upload_suppliermaster_new(request, popup_data_list, Test_mode)
        client = getClients(request)
        # check_data_class.app_name = table_data__array['appname']
        # check_data_class.table_name = table_data__array['Tablename']
        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = upload_suppliermaster_new(request, popup_data_list, Test_mode)
        print("check", check_variable)
        return JsonResponse(check_variable, safe=False)

    return render(request, 'Supplier_Management/supplier_upload.html')


def address_type(request):
    client = getClients(request)
    address_type_data = list(
        OrgAddressMap.objects.filter(del_ind=False).values('address_guid', 'address_number', 'address_type',
                                                           'company_id'))
    dropdown_db_values = list(
        FieldTypeDesc.objects.filter(field_name='address_type', del_ind=False).values('field_type_id',
                                                                                      'field_type_desc'
                                                                                      ))
    address_data = list(
        OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                        'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                                        'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                        'country_code',
                                                        'language_id', 'time_zone'))

    upload_data_OrgCompanies = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    return render(request, 'Address_Data/address_type.html',
                  {'address_type_data': address_type_data,
                   'dropdown_db_values': dropdown_db_values,
                   'upload_data_OrgCompanies': upload_data_OrgCompanies,
                   'address_data': address_data,
                   'inc_nav': True})


def address(request):
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    country_list = get_country_data()
    time_zone_data = list(TimeZone.objects.filter(del_ind=False).values('time_zone', 'description'))

    address_data = list(
        OrgAddress.objects.filter(del_ind=False).values('address_guid', 'address_number', 'title', 'name1', 'name2',
                                                        'street', 'area', 'landmark', 'city', 'postal_code', 'region',
                                                        'mobile_number', 'telephone_number', 'fax_number', 'email',
                                                        'country_code',
                                                        'language_id', 'time_zone'))

    return render(request, 'Address_Data/address.html',
                  {'address_data': address_data, 'language_list': language_list, 'country_list': country_list,
                   'time_zone_data': time_zone_data,
                   'inc_nav': True})


def extract_approverlimit_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="APPROVAL LIMIT.CSV"'

    writer = csv.writer(response)

    writer.writerow(['APPROVER_USERNAME', 'APP_CODE_ID', 'COMPANY_ID', 'del_ind'])

    approverlimit = django_query_instance.django_filter_query(ApproverLimit,
                                                              {'del_ind': False}, None,
                                                              ['approver_username', 'app_code_id', 'company_id',
                                                               'del_ind'])
    approverlim_data = query_update_del_ind(approverlimit)

    for approverlimitdata in approverlim_data:
        approverlimitdata_info = [approverlimitdata['approver_username'], approverlimitdata['app_code_id'],
                                  approverlimitdata['company_id'], approverlimitdata['del_ind']]
        writer.writerow(approverlimitdata_info)

    return response


def extract_approverlimitval_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="APPROVAL LIMIT VALUE.CSV"'

    writer = csv.writer(response)

    writer.writerow(['APP_CODE_ID', 'UPPER_LIMIT_VALUE', 'APP_TYPES', 'CURRENCY_ID', 'COMPANY_ID', 'del_ind'])

    approverlimitval = django_query_instance.django_filter_query(ApproverLimitValue,
                                                                 {'del_ind': False}, None,
                                                                 ['app_code_id', 'upper_limit_value', 'app_types',
                                                                  'currency_id', 'company_id', 'del_ind'])
    approverlim_data = query_update_del_ind(approverlimitval)

    for approverlimitvaldata in approverlim_data:
        approverlimitvaldata_info = [approverlimitvaldata['app_code_id'], approverlimitvaldata['upper_limit_value'],
                                     approverlimitvaldata['app_types'], approverlimitvaldata['currency_id'],
                                     approverlimitvaldata['company_id'], approverlimitvaldata['del_ind']]

        writer.writerow(approverlimitvaldata_info)

    return response


def extract_spendlimit_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="SPEND LIMIT.CSV"'

    writer = csv.writer(response)

    writer.writerow(['SPEND_CODE_ID', 'SPENDER_USERNAME', 'COMPANY_ID', 'del_ind'])
    # get only active record

    spendlimitvals = django_query_instance.django_filter_query(SpendLimitId,
                                                               {'del_ind': False}, None,
                                                               ['spend_code_id', 'spender_username',
                                                                'company_id', 'del_ind'])
    spendlim_data = query_update_del_ind(spendlimitvals)

    for spendlimitval in spendlim_data:
        spendlimitval_info = [spendlimitval['spend_code_id'], spendlimitval['spender_username'],
                              spendlimitval['company_id'], spendlimitval['del_ind']]
        writer.writerow(spendlimitval_info)

    return response


def extract_spendlimitval_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="SPEND LIMIT VALUE.CSV"'

    writer = csv.writer(response)

    writer.writerow(['SPEND_CODE_ID', 'UPPER_LIMIT_VALUE', 'COMPANY_ID', 'CURRENCY_ID', 'del_ind'])

    spendlimitvalues = django_query_instance.django_filter_query(SpendLimitValue, {'del_ind': False}, None,
                                                                 ['spend_code_id', 'upper_limit_value', 'company_id',
                                                                  'currency_id', 'del_ind'])
    spendlim_data = query_update_del_ind(spendlimitvalues)

    for spendlimitvaluedata in spendlim_data:
        spendlimitvaluedata_info = [spendlimitvaluedata['spend_code_id'], spendlimitvaluedata['upper_limit_value'],
                                    spendlimitvaluedata['company_id'],
                                    spendlimitvaluedata['currency_id'], spendlimitvaluedata['del_ind']]
        writer.writerow(spendlimitvaluedata_info)

    return response


def extract_spendlimit_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Spend_Limit.CSV"'

    writer = csv.writer(response)

    writer.writerow(['SPEND_CODE_ID', 'SPENDER_USERNAME', 'COMPANY_ID', 'del_ind'])

    return response


def extract_address_type_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ADDRESS TYPES.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ADDRESS_NUMBER', 'ADDRESS_TYPE', 'COMPANY_ID', 'del_ind'])

    address_type = django_query_instance.django_filter_query(OrgAddressMap,
                                                             {'del_ind': False}, None,
                                                             ['address_number', 'address_type', 'company_id',
                                                              'del_ind'])
    address_type_data = query_update_del_ind(address_type)

    for addresstypedata in address_type_data:
        address_type_info = [addresstypedata['address_number'],
                             addresstypedata['address_type'],
                             addresstypedata['company_id'],
                             addresstypedata['del_ind']]
        writer.writerow(address_type_info)

    return response


def extract_address_type_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Address_Types_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ADDRESS_NUMBER', 'ADDRESS_TYPE', 'COMPANY_ID', 'del_ind'])

    return response


def extract_glaccount_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DETERMINE_GL_ACCOUNT.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'GL_ACC_NUM', 'GL_ACC_DEFAULT', 'ACCOUNT_ASSIGN_CAT',
                     'COMPANY_ID', 'ITEM_FROM_VALUE', 'ITEM_TO_VALUE', 'CURRENCY_ID', 'del_ind'])

    glaccount = django_query_instance.django_filter_query(DetermineGLAccount,
                                                          {'del_ind': False}, None,
                                                          ['prod_cat_id', 'gl_acc_num',
                                                           'gl_acc_default', 'account_assign_cat', 'company_id',
                                                           'item_to_value', 'item_from_value', 'currency_id',
                                                           'del_ind'])

    glaccount_data = query_update_del_ind(glaccount)

    for glaccountdata in glaccount_data:
        glaccount_info = [glaccountdata['prod_cat_id'],
                          glaccountdata['gl_acc_num'], glaccountdata['gl_acc_default'],
                          glaccountdata['account_assign_cat'],
                          glaccountdata['company_id'], glaccountdata['item_from_value'],
                          glaccountdata['item_to_value'], glaccountdata['currency_id'], glaccountdata['del_ind']]

        writer.writerow(glaccount_info)

    return response


def extract_glaccount_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Determine_GL_Account_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PROD_CAT_ID', 'GL_ACC_NUM', 'GL_ACC_DEFAULT', 'ACCOUNT_ASSIGN_CAT',
                     'COMPANY_ID', 'ITEM_FROM_VALUE', 'ITEM_TO_VALUE', 'CURRENCY_ID', 'del_ind'])

    return response


def extract_pgrp_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain_Purchasing_Group.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PURCHASE GROUP ID', 'DESCRIPTION', 'PORG ID', 'OBJECT ID', 'del_ind'])

    purgrp = django_query_instance.django_filter_query(OrgPGroup,
                                                       {'del_ind': False}, None,
                                                       ['pgroup_id', 'description', 'porg_id', 'object_id',
                                                        'del_ind'])

    purgrp_data = query_update_del_ind(purgrp)

    for purgrpdata in purgrp_data:
        purgrp_info = [purgrpdata['pgroup_id'], purgrpdata['description'],
                       purgrpdata['porg_id'], purgrpdata['object_id'], purgrpdata['del_ind']]

        writer.writerow(purgrp_info)

    return response


def extract_pgrp_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain_Purchasing_Group_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PURCHASE GROUP ID', 'DESCRIPTION', 'PORG ID', 'OBJECT ID', 'del_ind'])

    return response



def extract_porg_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain_Purchasing_Organisation.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PURCHASE ORGANISATION ID', 'DESCRIPTION', 'COMPANY ID', 'OBJECT ID', 'del_ind'])

    purorg = django_query_instance.django_filter_query(OrgPorg,
                                                       {'del_ind': False}, None,
                                                       ['porg_id', 'description', 'company_id', 'object_id',
                                                        'del_ind'])

    purorg_data = query_update_del_ind(purorg)

    for purorgdata in purorg_data:
        purorg_info = [purorgdata['porg_id'], purorgdata['description'],
                       purorgdata['company_id'], purorgdata['object_id'], purorgdata['del_ind']]

        writer.writerow(purorg_info)

    return response


def extract_porg_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Maintain_Purchasing_Organisation_Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['PURCHASE ORGANISATION ID', 'DESCRIPTION', 'COMPANY ID', 'OBJECT ID', 'del_ind'])

    return response



def upload_prod_cat_images(request):
    """

    :param request:
    :return:
    """
    status = {}
    update_user_info(request)
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    file_name = request.POST.get('file_name')
    prod_cat = request.POST.get('prod_cat_id')
    save_prod_cat_image_to_db(prod_cat, file_name, attached_file)
    return JsonResponse(status, safe=False)


def extract_orgcompany_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ORGCOMPANY.CSV"'

    writer = csv.writer(response)

    writer.writerow(['OBJECT_ID', 'NAME1', 'NAME2', 'COMPANY_ID', 'del_ind'])

    orgcompany = django_query_instance.django_filter_query(OrgCompanies,
                                                           {'del_ind': False}, None,
                                                           ['object_id', 'name1', 'name2',
                                                            'company_id', 'del_ind'])
    orgcompany_data = query_update_del_ind(orgcompany)

    for orgcompanydata in orgcompany_data:
        orgcompanydata_info = [orgcompanydata['object_id'], orgcompanydata['name1'], orgcompanydata['name2'],
                               orgcompanydata['company_id'], orgcompanydata['del_ind']]
        writer.writerow(orgcompanydata_info)

    return response


def extract_address_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ADDRESS.CSV"'

    writer = csv.writer(response)

    writer.writerow(['ADDRESS_NUMBER', 'TITLE', 'NAME1', 'NAME2', 'STREET', 'AREA', 'LANDMARK', 'CITY',
                     'postal_code', 'REGION', 'MOBILE_NUMBER', 'TELEPHONE_NUMBER', 'FAX_NUMBER', 'EMAIL',
                     'COUNTRY_CODE',
                     'LANGUAGE_ID', 'TIME_ZONE', 'del_ind'])

    address = django_query_instance.django_filter_query(OrgAddress,
                                                        {'del_ind': False}, None,
                                                        ['address_number', 'title', 'name1', 'name2', 'street', 'area',
                                                         'landmark', 'city', 'postal_code', 'region', 'mobile_number',
                                                         'telephone_number', 'fax_number', 'email', 'country_code',
                                                         'language_id', 'time_zone',
                                                         'del_ind'])
    address_data = query_update_del_ind(address)

    for addressdata in address_data:
        address_info = [addressdata['address_number'],
                        addressdata['title'],
                        addressdata['name1'],
                        addressdata['name2'],
                        addressdata['street'],
                        addressdata['area'],
                        addressdata['landmark'],
                        addressdata['city'],
                        addressdata['postal_code'],
                        addressdata['region'],
                        addressdata['mobile_number'],
                        addressdata['telephone_number'],
                        addressdata['fax_number'],
                        addressdata['email'],
                        addressdata['country_code'],
                        addressdata['language_id'],
                        addressdata['time_zone'],
                        addressdata['del_ind']]
        writer.writerow(address_info)

    return response


def upload_cust_prod_cat(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    upload_cust_prod_catogories = django_query_instance.django_filter_query(UnspscCategoriesCust,
                                                                            {'client': client, 'del_ind': False}, None,
                                                                            ['prod_cat_guid', 'prod_cat_id'])

    product_cat_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(UnspscCategoriesCust,
                                                                                                {'client': client,
                                                                                                 'del_ind': False},
                                                                                                'prod_cat_id',
                                                                                                None)
    prod_cat_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                              {'prod_cat_id__in': product_cat_list,
                                                               'del_ind': False},
                                                              None,
                                                              ['prod_cat_id', 'language_id', 'category_desc'])
    for prod_cat in upload_cust_prod_catogories:
        prod_cat['prod_cat_desc'] = ' '
        for product_cat in prod_cat_desc:
            if prod_cat['prod_cat_id'] == product_cat['prod_cat_id']:
                if product_cat['language_id'] == global_variables.GLOBAL_USER_LANGUAGE.language_id:
                    prod_cat['prod_cat_desc'] = product_cat['category_desc']
                break

    for prod in upload_cust_prod_catogories:
        if prod['prod_cat_desc'] is None:
            prod['prod_cat_desc'] = ' '

        if django_query_instance.django_existence_check(ImagesUpload, {'client': global_variables.GLOBAL_CLIENT,
                                                                       'image_default': True,
                                                                       'image_id': prod['prod_cat_id'],
                                                                       'image_type': CONST_UNSPSC_IMAGE_TYPE,
                                                                       'del_ind': False}):
            prod['image_url'] = django_query_instance.django_filter_value_list_ordered_by_distinct_query(ImagesUpload, {
                'client': global_variables.GLOBAL_CLIENT, 'image_default': True, 'image_id': prod['prod_cat_id'],
                'image_type': CONST_UNSPSC_IMAGE_TYPE, 'del_ind': False
            }, 'image_url', None)[0]

        else:
            prod['image_url'] = ""

    upload_ProdCat = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))

    for prod_cat_desc in upload_ProdCat:

        if prod_cat_desc['prod_cat_desc'] == None:
            prod_cat_desc['prod_cat_desc'] = ''

    # upload_dropdown = ~Q(prod_cat_id=[upload_ProdCat, product_cat_list])
    #
    # print(upload_dropdown)

    content_managment_settings = 'content_managment_settings'

    return render(request,
                  'Customer_Product_Category/customer_product_category.html',
                  {'upload_cust_prod_cat': upload_cust_prod_catogories,
                   'upload_ProdCat': upload_ProdCat,
                   # 'upload_dropdown':upload_dropdown,
                   'content_managment_settings': content_managment_settings,
                   'inc_nav': True})


def upload_cust_prod_cat_desc(request):
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    upload_cust_prod_desc_catogories = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                                                 {'client': client, 'del_ind': False},
                                                                                 None,
                                                                                 ['prod_cat_desc_guid', 'prod_cat_id',
                                                                                  'category_desc', 'language_id'])

    product_cat_list = django_query_instance.django_filter_value_list_ordered_by_distinct_query(
        UnspscCategoriesCustDesc,
        {'client': client,
         'del_ind': False},
        'prod_cat_id',
        None)
    prod_cat_desc = django_query_instance.django_filter_query(UnspscCategoriesCustDesc,
                                                              {'prod_cat_id__in': product_cat_list,
                                                               'del_ind': False},
                                                              None,
                                                              ['prod_cat_id', 'language_id', 'category_desc'])

    upload_language = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))

    for prod_cat in upload_cust_prod_desc_catogories:
        prod_cat['prod_cat_desc'] = ' '
        for product_cat in prod_cat_desc:
            if prod_cat['prod_cat_id'] == product_cat['prod_cat_id']:
                if product_cat['language_id'] == global_variables.GLOBAL_USER_LANGUAGE.language_id:
                    prod_cat['prod_cat_desc'] = product_cat['category_desc']
                break

    for prod in upload_cust_prod_desc_catogories:
        if prod['prod_cat_desc'] is None:
            prod['prod_cat_desc'] = ' '

    upload_ProdCat = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))

    for prod_cat_desc in upload_ProdCat:

        if prod_cat_desc['prod_cat_desc'] == None:
            prod_cat_desc['prod_cat_desc'] = ''

    content_managment_settings = 'content_managment_settings'

    return render(request,
                  'Customer_Product_Category/customer_product_category_description.html',
                  {'upload_cust_prod_cat_desc': upload_cust_prod_desc_catogories,
                   'upload_languages': upload_language,
                   'upload_ProdCat': upload_ProdCat,
                   'content_managment_settings': content_managment_settings,
                   'inc_nav': True})


def org_companies(request):
    client = getClients(request)
    upload_orgcompany = list(
        OrgCompanies.objects.filter(client=client, del_ind=False).values('company_guid', 'object_id', 'name1', 'name2',
                                                                         'company_id'))
    upload_data_Orgmodel = list(OrgModel.objects.filter(client=client, del_ind=False).values('object_id'))
    for object_id in upload_orgcompany:
        if object_id['object_id'] == None:
            object_id['object_id'] = ''
    master_data_settings = 'master_data_settings'
    return render(request, 'Organizational_Data/org_companies.html',
                  {'org_companies': upload_orgcompany, 'upload_data_Orgmodel': upload_data_Orgmodel,
                   'master_data_settings': master_data_settings, 'inc_nav': True})


def purchasing_org(request):
    client = getClients(request)
    upload_porg = list(
        OrgPorg.objects.filter(client=client, del_ind=False).values('porg_guid', 'porg_id', 'object_id', 'description',
                                                                    'company_id'))
    upload_data_Orgmodel = list(OrgModel.objects.filter(client=client, del_ind=False).values('object_id'))
    upload_data_OrgCompanies = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    master_data_settings = 'master_data_settings'

    for object_id in upload_porg:
        if object_id['object_id'] == None:
            object_id['object_id'] = ''

    return render(request, 'Organizational_Data/purchase_org.html',
                  {'purchasing_org': upload_porg, 'upload_data_Orgmodel': upload_data_Orgmodel,
                   'upload_data_OrgCompanies': upload_data_OrgCompanies, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def purchasing_grp(request):
    client = getClients(request)
    upload_pgrp = list(
        OrgPGroup.objects.filter(client=client, del_ind=False).values('pgroup_guid', 'pgroup_id', 'object_id',
                                                                      'description', 'porg_id'))
    upload_data_Orgmodel = list(OrgModel.objects.filter(client=client, del_ind=False).values('object_id'))
    upload_data_OrgPGroup = list(OrgPGroup.objects.filter(client=client, del_ind=False).values('porg_id'))
    master_data_settings = 'master_data_settings'

    for object_id in upload_pgrp:
        if object_id['object_id'] == None:
            object_id['object_id'] = ''

    return render(request, 'Organizational_Data/purchase_grp.html',
                  {'purchasing_grp': upload_pgrp, 'upload_data_Orgmodel': upload_data_Orgmodel,
                   'upload_data_OrgPGroup': upload_data_OrgPGroup, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def account_assignment(request):
    client = getClients(request)
    upload_accassignment = get_configuration_data(AccountingDataDesc, {'client': client, 'del_ind': False},
                                                  ['acc_desc_guid', 'account_assign_value',
                                                   'description', 'account_assign_cat',
                                                   'company_id', 'language_id'])
    upload_accassvalues = get_configuration_data(AccountingData, {'del_ind': False},
                                                 ['account_assign_value', 'account_assign_cat',
                                                  'company_id'])

    upload_data_acccat = get_configuration_data(AccountAssignmentCategory, {'del_ind': False}, ['account_assign_cat'])
    upload_data_company = get_configuration_data(OrgCompanies, {'del_ind': False}, ['company_id'])
    upload_data_language = get_configuration_data(Languages, {'del_ind': False}, ['language_id'])
    master_data_settings = 'master_data_settings'
    return render(request, 'Accounting_Data/account_assignment_description.html',
                  {'account_assignment': upload_accassignment, 'upload_data_company': upload_data_company,
                   'upload_data_acccat': upload_data_acccat, 'upload_data_language': upload_data_language,
                   'upload_accassvalues': upload_accassvalues, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def det_gl_acc(request):
    client = getClients(request)
    prod_catogories = list(
        UnspscCategoriesCust.objects.filter(client=client, del_ind=False).values('prod_cat_id'))

    upload_gl_acc_db = list(
        DetermineGLAccount.objects.filter(client=client, del_ind=False).values('det_gl_acc_guid', 'prod_cat_id',
                                                                               'item_from_value', 'item_to_value',
                                                                               'gl_acc_num',
                                                                               'gl_acc_default', 'company_id',
                                                                               'account_assign_cat', 'currency_id'))
    upload_gl_acc = []
    for data in upload_gl_acc_db:

        if data['gl_acc_num'] == None:
            data['gl_acc_num'] = ''

        data_dict = {
            'det_gl_acc_guid': data['det_gl_acc_guid'],
            'prod_cat_id': data['prod_cat_id'],
            'item_from_value': data['item_from_value'],
            'item_to_value': data['item_to_value'],
            'gl_account': data['gl_acc_num'],
            'gl_acc_default': str(data['gl_acc_default']),
            'company_id': data['company_id'],
            'account_assign_cat': data['account_assign_cat'],
            'currency_id': data['currency_id'],

        }
        upload_gl_acc.append(data_dict)

    upload_value_glacc = list(
        AccountingData.objects.filter(client=client, del_ind=False).values('account_assign_value'))
    upload_value_accasscat = list(
        AccountAssignmentCategory.objects.filter(~Q(account_assign_cat='GLACC'), del_ind=False).values(
            'account_assign_cat'))
    upload_value_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_value_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))

    return render(request, 'GL_Account/determine_gl_account.html',
                  {'upload_gl_acc': upload_gl_acc, 'upload_value_glacc': upload_value_glacc,
                   'upload_value_accasscat': upload_value_accasscat,
                   'upload_value_currency': upload_value_currency,
                   'upload_value_company': upload_value_company, 'prod_catogories': prod_catogories,
                   'inc_nav': True})


def approval_type(request):
    upload_apptype = list(ApproverType.objects.filter(del_ind=False).values('app_types', 'appr_type_desc'))
    dropdown_db_values = list(
        FieldTypeDesc.objects.filter(field_name='approval_type', del_ind=False, used_flag=0).values('field_type_id',
                                                                                                    'field_type_desc'
                                                                                                    ))
    dropdown_db_values_onload = list(
        FieldTypeDesc.objects.filter(field_name='approval_type', del_ind=False).values('field_type_id',
                                                                                       'field_type_desc'
                                                                                       ))
    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_type.html',
                  {'approval_type': upload_apptype, 'master_data_settings': master_data_settings,
                   'inc_nav': True,
                   'dropdown_db_values': dropdown_db_values,
                   'dropdown_db_values_onload': dropdown_db_values_onload})


def work_flow_schema(request):
    client = getClients(request)
    upload_wfschema = get_configuration_data(
        WorkflowSchema, {'client': client, 'del_ind': False}, ['workflow_schema_guid', 'workflow_schema',
                                                               'app_types', 'company_id'])
    upload_data_company = get_configuration_data(OrgCompanies, {'client': client, 'del_ind': False}, ['company_id'])
    upload_data_apptypes = get_configuration_data(ApproverType, {'del_ind': False}, ['app_types'])
    dropdown_db_values = list(
        FieldTypeDesc.objects.filter(field_name='workflow_schema', del_ind=False).values(
            'field_type_id',
            'field_type_desc'
        ))
    master_data_settings = 'master_data_settings'
    return render(request, 'Work_Flow_Data/work_flow_schema.html',
                  {'work_flow_schema': upload_wfschema, 'upload_data_company': upload_data_company,
                   'upload_data_apptypes': upload_data_apptypes,
                   'dropdown_db_values': dropdown_db_values,
                   'master_data_settings': master_data_settings,
                   'inc_nav': True})


def spend_limit_value(request):
    client = getClients(request)
    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=client, del_ind=False).values('spend_lim_value_guid', 'spend_code_id',
                                                                            'upper_limit_value', 'currency_id',
                                                                            'company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    master_data_settings = 'master_data_settings'
    return render(request, 'Spend_Limit_data/spend_limit_value.html',
                  {'spend_limit_value': upload_spndlimval, 'upload_data_company': upload_data_company,
                   'upload_data_currency': upload_data_currency, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def approval_limit(request):
    client = getClients(request)

    upload_applimit = list(
        ApproverLimit.objects.filter(client=client, del_ind=False).values('app_guid', 'approver_username',
                                                                          'app_code_id', 'company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_app_code_id = list(
        ApproverLimitValue.objects.filter(client=client, del_ind=False).values('app_code_id'))

    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))

    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_limit.html',
                  {'approval_limit': upload_applimit, 'upload_data_company': upload_data_company,
                   'upload_data_app_code_id': upload_data_app_code_id,
                   'master_data_settings': master_data_settings,
                   'user_details': user_details,
                   'inc_nav': True})


def approval_limit_value(request):
    client = getClients(request)
    upload_applimval = list(
        ApproverLimitValue.objects.filter(client=client, del_ind=False).values('app_lim_dec_guid', 'app_types',
                                                                               'app_code_id', 'currency_id',
                                                                               'upper_limit_value', 'company_id'))
    upload_data_apptypes = list(ApproverType.objects.filter(del_ind=False).values('app_types'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    # upload_data_company = list(OrgCompanies.objects.filter(del_ind=False).values('company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))

    master_data_settings = 'master_data_settings'
    return render(request, 'Approval_Data/approval_limit_value.html',
                  {'approval_limit_value': upload_applimval, 'upload_data_apptypes': upload_data_apptypes,
                   'upload_data_currency': upload_data_currency, 'upload_data_company': upload_data_company,
                   'master_data_settings': master_data_settings, 'inc_nav': True})


def spend_limit_id(request):
    client = getClients(request)
    upload_spndlimid = list(
        SpendLimitId.objects.filter(client=client, del_ind=False).values('spend_guid', 'spend_code_id',
                                                                         'spender_username', 'company_id'))

    upload_spndlimval = list(
        SpendLimitValue.objects.filter(client=client, del_ind=False).values('spend_lim_value_guid', 'spend_code_id',
                                                                            'upper_limit_value', 'currency_id',
                                                                            'company_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))
    master_data_settings = 'master_data_settings'
    return render(request, 'Spend_Limit_data/spend_limit_id.html',
                  {'spend_limit_id': upload_spndlimid, 'upload_data_company': upload_data_company,
                   'spend_limit_value': upload_spndlimval,
                   'master_data_settings': master_data_settings, 'user_details': user_details, 'inc_nav': True})


def work_flow_accounting(request):
    client = getClients(request)
    upload_wfacc = list(
        WorkflowACC.objects.filter(client=client, del_ind=False).values('workflow_acc_guid', 'app_username',
                                                                        'acc_value', 'sup_acc_value',
                                                                        'account_assign_cat', 'sup_account_assign_cat',
                                                                        'company_id', 'sup_company_id', 'currency_id'))
    upload_data_acccat = list(AccountAssignmentCategory.objects.filter(del_ind=False).values('account_assign_cat'))
    upload_data_currency = list(Currency.objects.filter(del_ind=False).values('currency_id'))
    upload_data_company = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    upload_data_OrgCompanies = list(OrgCompanies.objects.filter(client=client, del_ind=False).values('company_id'))
    user_details = list(UserData.objects.filter(is_active=True, client=client, del_ind=False).values('username'))
    master_data_settings = 'master_data_settings'
    return render(request, 'Work_Flow_Data/work_flow_accounting.html',
                  {'work_flow_accounting': upload_wfacc, 'upload_data_acccat': upload_data_acccat,
                   'upload_data_currency': upload_data_currency, 'upload_data_company': upload_data_company,
                   'upload_data_OrgCompanies': upload_data_OrgCompanies, 'master_data_settings': master_data_settings
                      , 'user_details': user_details, 'inc_nav': True})
