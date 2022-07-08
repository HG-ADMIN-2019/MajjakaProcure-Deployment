import datetime
import json
import os
# import cv2
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from eProc_Basic.Utilities.constants.constants import CONST_FT_ITEM_EFORM, CONST_QUANTITY_BASED_DISCOUNT
from eProc_Basic.Utilities.functions.dict_check_key import checkKey
from eProc_Basic.Utilities.functions.dictionary_key_to_list import dictionary_key_to_list
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt, encrypt
from eProc_Basic.Utilities.functions.guid_generator import dynamic_guid_generator, guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.query_append_id_desc import AppendIdDesc
from eProc_Basic.Utilities.functions.query_basic_data_append_desc import get_unspsc_append_desc_data, \
    get_supplier_append_desc_data, get_uom_append_desc_data, get_currency_append_desc_data, \
    get_country_append_desc_data, get_language_append_desc_data, catalog_append_desc_data, get_basic_data
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.global_defination.global_variables import GLOBAL_FILENAME_COUNT
from eProc_Basic.Utilities.messages.messages import MSG129, MSG130
from eProc_Catalog.Utilities.catalog_specific import save_image_to_db, save_product_images
from eProc_Configuration.models import ProductsDetail, Country, Currency, SupplierMaster, UnitOfMeasures, Languages, \
    Catalogs, ImagesUpload, UnspscCategories, FreeTextDetails, EformFieldConfig
from eProc_Form_Builder.Utilities.form_builder_generic import FormBuilder
from eProc_Form_Builder.models import EformFieldData
from eProc_Manage_Content.Utilities.manage_content_generic import get_product_details_image_eform, get_eform_details
from eProc_Manage_Content.Utilities.manage_content_specific import save_product_details_eform, \
    save_product_specification, save_catalog_to_db, get_assigned_unssigned_product_id_list, save_catalog_mapping, \
    CatalogMappingAction
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_cat, get_supplier_first_second_name
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def get_product_details(request, product_id):
    """

    """
    update_user_info(request)

    product_details = []
    country_of_origin_id = ''
    unit_id = ''
    new_product_id = ''
    language_id = ''
    supplier_id = ''
    catalog_id = ''
    prod_cat_id = ''
    currency_id = ''
    encrypt_new_product_id = ''
    prod_img_detail = []
    eform_configured = []
    eform_edit_flag = 0
    product_existence_flag = False
    product_specification = []
    if product_id != 'None':
        product_existence_flag = True
        template = 'ManageContentDetail/display_edit_product_detail.html'
        product_id = decrypt(product_id)
        # get product details and image information
        product_details, prod_img_detail, eform_configured, product_specification, eform_edit_flag = get_product_details_image_eform(
            product_id)

        # if product_id exist then update default basic data
        if product_details:
            country_of_origin_id = product_details.country_of_origin_id
            currency_id = product_details.currency_id
            unit_id = product_details.unit_id
            language_id = product_details.language_id
            supplier_id = product_details.supplier_id
            prod_cat_id = product_details.prod_cat_id
    else:
        new_product_id = dynamic_guid_generator(16)
        encrypt_new_product_id = encrypt(new_product_id)
        template = 'ManageContentDetail/display_edit_new_product_detail.html'
    # get basic details
    country_desc, currency_desc, unit_desc, \
    language_desc, supplier_desc, unspsc_desc = get_basic_data(
        country_of_origin_id, currency_id, unit_id, language_id, supplier_id, prod_cat_id,
        global_variables.GLOBAL_USER_LANGUAGE)

    client = global_variables.GLOBAL_CLIENT
    product_category = get_prod_cat(request, prod_det=None)
    supplier_details = get_supplier_first_second_name(client)

    # print(eform_configured)
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'product_details': product_details,
        'country_desc': country_desc,
        'unit_desc': unit_desc,
        'language_desc': language_desc,
        'supplier_desc': supplier_desc,
        'unspsc_desc': unspsc_desc,
        'currency_desc': currency_desc,
        'prod_img_detail': prod_img_detail,
        'eform_configured': eform_configured,
        'eform_edit_flag': eform_edit_flag,
        'product_specification': product_specification,
        'new_product_id': new_product_id,
        'product_existence_flag': product_existence_flag,
        'encrypt_new_product_id': encrypt_new_product_id,
        'product_category': product_category,
        'supplier_details': supplier_details
    }

    return render(request, template, context)


def save_product_details_spec_images_eform(request):
    """

    """
    update_user_info(request)
    product_not_exist = ''
    eform_configured = {}
    product_info_id = None
    tiered_pricing = False
    ui_data = request.POST
    attached_file = request.FILES
    converted_dict = dict(ui_data.lists())
    data = json.loads(request.POST['update'])
    eform_configured = json.loads(request.POST['eform_configured'])
    product_existence_flag = json.loads(request.POST['product_existence_flag'])
    product_specification_data = json.loads(request.POST['product_specification_data'])
    form_id = ''
    if eform_configured:
        if product_existence_flag == 0 or 'False':
            form_id = save_product_details_eform(eform_configured, data['product_id'])
        field_type_list = dictionary_key_to_list(eform_configured, 'field_type')
        if CONST_QUANTITY_BASED_DISCOUNT in field_type_list:
            tiered_pricing = True
    if product_specification_data:
        if product_existence_flag == 0 or 'False':
            product_info_id = save_product_specification(product_specification_data, data['product_id'])
    save_product_images(attached_file, data['product_id'])
    # save images
    # if checkKey(converted_dict, 'Prod_cat'):
    #     prod_cat = converted_dict['Prod_cat']
    #     file_name = converted_dict['file_name']
    #     default_image = [True if img_flag else False for img_flag in converted_dict['default_image_value']]
    #     save_image_to_db(prod_cat, file_name, attached_file, default_image)
    # if ProductsDetail.objects.filter(product_id=data['product_id']).exists():
    # check for discount

    if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                     'product_id': data['product_id']}):
        django_query_instance.django_update_query(ProductsDetail,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'product_id': data['product_id']},
                                                  {'short_desc': data["short_desc"],
                                                   'long_desc': data['long_desc'],
                                                   'supplier_id': data['supplier_id'],
                                                   'cust_prod_cat_id': data['prod_cat_id'],
                                                   'prod_type': data['product_type'],
                                                   'value_min':data['value_min'],
                                                   'price_on_request': False,
                                                   'unit': UnitOfMeasures.objects.get(
                                                       uom_id=data['unit']),
                                                   'price_unit': data['price_unit'],
                                                   'currency': Currency.objects.get(
                                                       currency_id=data['currency']),
                                                   'price': data['price'],
                                                   'manufacturer': data['manufacturer'],
                                                   'manu_part_num': data['manu_prod'],
                                                   'prod_cat_id': UnspscCategories.objects.get(
                                                       prod_cat_id=data['unspsc']),
                                                   'brand': data['brand'],
                                                   'lead_time': data['lead_time'],
                                                   'quantity_avail': data[
                                                       'quantity_avail'],
                                                   'quantity_min': data['quantity_min'],
                                                   'offer_key': data['offer_key'],
                                                   'country_of_origin': Country.objects.get(
                                                       country_code=data[
                                                           'country_of_origin']),
                                                   'language': Languages.objects.get(
                                                       language_id=data['language']),
                                                   'search_term1': data['search_term1'],
                                                   'search_term2': data['search_term2'],
                                                   'eform_id': form_id,
                                                   'product_info_id': product_info_id,
                                                   'changed_at': datetime.date.today(),
                                                   'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'supp_product_id': data['supplier_product_number'],
                                                   'external_link': data['product_webpage_link'],
                                                   'ctr_num': data['product_contract_num'],
                                                   'ctr_item_num':data['ctr_item_num'],
                                                   'ctr_name': data['product_contract_name'],
                                                   'manu_code_num': data['prd_manu_code_no'],
                                                   'quantity_max': data['quantity_max'],
                                                   'products_detail_source_system': data['product_source_system']
                                                   })
    else:
        django_query_instance.django_create_query(ProductsDetail,
                                                  {'client': global_variables.GLOBAL_CLIENT,
                                                   'catalog_item': guid_generator(),
                                                   'product_id': data['product_id'],
                                                   'short_desc': data["short_desc"],
                                                   'long_desc': data['long_desc'],
                                                   'value_min': data['value_min'],
                                                   'supplier_id': data['supplier_id'],
                                                   'cust_prod_cat_id': data['prod_cat_id'],
                                                   'prod_type': data['product_type'],
                                                   'price_on_request': False,
                                                   'unit': UnitOfMeasures.objects.get(
                                                       uom_id=data['unit']),
                                                   'price_unit': data['price_unit'],
                                                   'currency': Currency.objects.get(
                                                       currency_id=data['currency']),
                                                   'price': data['price'],
                                                   'manufacturer': data['manufacturer'],
                                                   'manu_part_num': data['manu_prod'],
                                                   'prod_cat_id': UnspscCategories.objects.get(
                                                       prod_cat_id=data['unspsc']),
                                                   'brand': data['brand'],
                                                   'lead_time': data['lead_time'],
                                                   'quantity_avail': data[
                                                       'quantity_avail'],
                                                   'quantity_min': data['quantity_min'],
                                                   'offer_key': data['offer_key'],
                                                   'country_of_origin': Country.objects.get(
                                                       country_code=data[
                                                           'country_of_origin']),
                                                   'language': Languages.objects.get(
                                                       language_id=data['language']),
                                                   'search_term1': data['search_term1'],
                                                   'search_term2': data['search_term2'],
                                                   'eform_id': form_id,
                                                   'product_info_id': product_info_id,
                                                   'created_at': datetime.date.today(),
                                                   'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'changed_at': datetime.date.today(),
                                                   'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                   'supplier_product_info': data['supplier_product_number'],
                                                   'external_link': data['product_webpage_link'],
                                                   'ctr_num': data['product_contract_num'],
                                                   'ctr_item_num': data['ctr_item_num'],
                                                   'ctr_name': data['product_contract_name'],
                                                   'manu_code_num': data['prd_manu_code_no'],
                                                   'quantity_max': data['quantity_max'],
                                                   'products_detail_source_system': data['product_source_system']

                                                   })
    eform_configured, eform_edit_flag = get_eform_details(form_id)
    return JsonResponse(eform_configured, safe=False)


def save_catalog_db(request):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    catalog_data = JsonParser_obj.get_json_from_req(request)
    catalog_data_response = save_catalog_to_db(catalog_data)
    return JsonResponse(catalog_data_response, safe=False)


def generate_guid(request):
    """

    """
    catalog = {}
    catalog['catalog_id'] = dynamic_guid_generator(4)
    return JsonResponse(catalog, safe=False)


def get_assign_unassign_product(request):
    """

    """
    update_user_info(request)
    assign_unassign_data = JsonParser_obj.get_json_from_req(request)
    catalog_mapping_instance = CatalogMappingAction(assign_unassign_data['catalog_id'])
    product_id_list, freetext_id_list = catalog_mapping_instance.get_assigned_unssigned_product_id_list(
        assign_unassign_data)
    catalog_mapping_product_details = {'product_id_list': product_id_list, 'freetext_id_list': freetext_id_list}
    return JsonResponse(catalog_mapping_product_details, safe=False)


def assign_unassign_product_data(request):
    """

    """
    update_user_info(request)
    catalog_mapping_info = JsonParser_obj.get_json_from_req(request)
    catalog_mapping_instance = CatalogMappingAction(catalog_mapping_info['catalog_id'])
    catalog_mapping_instance.save_catalog_mapping(catalog_mapping_info)
    response = {}
    return JsonResponse(response, safe=False)


def activate_deactivate_catalog(request):
    """

    """
    catalog_active_flag_detail = JsonParser_obj.get_json_from_req(request)
    django_query_instance.django_update_query(Catalogs,
                                              {'client': global_variables.GLOBAL_CLIENT,
                                               'catalog_id': catalog_active_flag_detail['catalog_id'],
                                               'del_ind': False},
                                              {'is_active_flag': catalog_active_flag_detail['flag']})
    response = {}
    return JsonResponse(response, safe=False)


def save_data_upload(request):
    """

    """
    data = JsonParser_obj.get_json_from_req(request)

    for val in data:
        if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                         'product_id': val['product_id']}):
            # print(val['product_id'])
            django_query_instance.django_update_query(ProductsDetail,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'product_id': val['product_id']},
                                                      {'short_desc': val["short_desc"],
                                                       'long_desc': val['long_desc'],
                                                       'supplier_id': val['supplier_id'],
                                                       'cust_prod_cat_id': val['prod_cat_id'],
                                                       'product_type': val['product_type'],
                                                       'price_on_request': False,
                                                       'unit': UnitOfMeasures.objects.get(
                                                           uom_id=val['unit']),
                                                       'price_unit': val['price_unit'],
                                                       'currency': Currency.objects.get(
                                                           currency_id=val['currency']),
                                                       'price': val['price'],
                                                       'manufacturer': val['manufacturer'],
                                                       'manu_part_num': val['manu_prod'],
                                                       'prod_cat_id': UnspscCategories.objects.get(
                                                           prod_cat_id=val['unspsc']),
                                                       'brand': val['brand'],
                                                       'lead_time': val['lead_time'],
                                                       'quantity_avail': val[
                                                           'quantity_avail'],
                                                       'quantity_min': val['quantity_min'],
                                                       'offer_key': val['offer_key'],
                                                       'country_of_origin': Country.objects.get(
                                                           country_code=val[
                                                               'country_of_origin']),
                                                       'language': Languages.objects.get(
                                                           language_id=val['language']),
                                                       'search_term1': val['search_term1'],
                                                       'search_term2': val['search_term2'],
                                                       'eform_id': val['eform_id'],
                                                       'product_info_id': val['product_info_id'],
                                                       'changed_at': datetime.date.today(),
                                                       'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                       'supplier_product_info': val['supplier_product_number'],
                                                       'external_link': val['product_webpage_link'],
                                                       'ctr_num': val['product_contract_num'],
                                                       'products_detail_source_system': val['product_source_system']
                                                       })
            response = 0
        else:
            django_query_instance.django_create_query(ProductsDetail,
                                                      {'client': global_variables.GLOBAL_CLIENT,
                                                       'catalog_item': guid_generator(),
                                                       'product_id': val['product_id'],
                                                       'short_desc': val["short_desc"],
                                                       'long_desc': val['long_desc'],
                                                       'supplier_id': val['supplier_id'],
                                                       'cust_prod_cat_id': val['prod_cat_id'],
                                                       'product_type': val['product_type'],
                                                       'price_on_request': False,
                                                       'unit': UnitOfMeasures.objects.get(
                                                           uom_id=val['unit']),
                                                       'price_unit': val['price_unit'],
                                                       'currency': Currency.objects.get(
                                                           currency_id=val['currency']),
                                                       'price': val['price'],
                                                       'manufacturer': val['manufacturer'],
                                                       'manu_part_num': val['manu_prod'],
                                                       'prod_cat_id': UnspscCategories.objects.get(
                                                           prod_cat_id=val['unspsc']),
                                                       'brand': val['brand'],
                                                       'lead_time': val['lead_time'],
                                                       'quantity_avail': val[
                                                           'quantity_avail'],
                                                       'quantity_min': val['quantity_min'],
                                                       'offer_key': val['offer_key'],
                                                       'country_of_origin': Country.objects.get(
                                                           country_code=val[
                                                               'country_of_origin']),
                                                       'language': Languages.objects.get(
                                                           language_id=val['language']),
                                                       'search_term1': val['search_term1'],
                                                       'search_term2': val['search_term2'],
                                                       'eform_id': val['eform_id'],
                                                       'product_info_id': val['product_info_id'],
                                                       'created_at': datetime.date.today(),
                                                       'created_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                       'changed_at': datetime.date.today(),
                                                       'changed_by': global_variables.GLOBAL_LOGIN_USERNAME,
                                                       'supplier_product_info': val['supplier_product_number'],
                                                       'external_link': val['product_webpage_link'],
                                                       'ctr_num': val['product_contract_num'],
                                                       'products_detail_source_system': val['product_source_system']
                                                       })
            response = 1
    return JsonResponse(response, safe=False)


def get_image_details(request):
    """

    """
    client = global_variables.GLOBAL_CLIENT
    count = global_variables.GLOBAL_FILENAME_COUNT + 1
    image_details = list(
        ImagesUpload.objects.filter(client=client, del_ind=False).values(
            'image_id', 'image_number',
            'image_url', 'image_name', 'image_default', 'image_type', 'images_upload_source_system',
            'images_upload_destination_system', 'client'))
    imgtype = []
    img_client = []
    imgId = []
    imgName = []
    # imgarray = []
    imgarray2 = []

    print(image_details)
    for data in image_details:
        imgtype.append(data['image_type'])
        img_client.append(data['client'])
        imgId.append(data['image_id'])
        imgName.append(data['image_name'])

        imgarray = []
        imgarray.append(data['image_type'])
        imgarray.append(data['client'])
        imgarray.append(data['image_id'])

        imgPath = '/'.join(imgarray)
        print(imgPath)
        dir_check = "C:/Users/Lenovo/Downloads/" + imgPath

        if os.path.isdir(dir_check):
            new_folder = imgarray[0] + '(' + str(count + 1) + ')'
            imgarray2.append(new_folder)
            imgarray2.append(img_client[0])
            imgarray2.append(imgId[0])
            imgPath2 = '/'.join(imgarray2)
            final_path = "C:/Users/Lenovo/Downloads/" + imgPath2
            global_variables.GLOBAL_FILENAME_COUNT = modify_count(count)
        else:
            final_path = "C:/Users/Lenovo/Downloads/" + imgPath

        os.makedirs(final_path, mode=0o666)
        filename = data['image_name']
        path = r'media/' + imgPath + '/' + filename
        # img = cv2.imread(path)
        os.chdir(final_path)
        # cv2.imwrite(filename, img)
        os.chdir(final_path)
        imgPath = ''

    res = 1

    context = {
        'image_details': image_details,
        'res': res,
    }

    return JsonResponse(context, safe=False)


def modify_count(count):
    global_variables.GLOBAL_FILENAME_COUNT = count + 1
    print("count = ", global_variables.GLOBAL_FILENAME_COUNT)
    return global_variables.GLOBAL_FILENAME_COUNT


@login_required
@transaction.atomic
def delete_freetext_form(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    freetext_id_list = JsonParser_obj.get_json_from_req(request)
    freetext_info = FormBuilder().delete_freetext(freetext_id_list['data'])
    response = {'freetext_info': freetext_info,
                'success_message': MSG130}
    return JsonResponse(response, safe=False)


def delete_product(request):
    """
    :param request:
    :return:
    """
    update_user_info(request)
    product_id_list = JsonParser_obj.get_json_from_req(request)
    product_info = FormBuilder().delete_product_item(product_id_list['data'])
    response = {'product_info': product_info,
                'success_message': MSG130}
    return JsonResponse(response, safe=False)
