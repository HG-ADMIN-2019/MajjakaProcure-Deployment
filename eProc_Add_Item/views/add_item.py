import datetime
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from eProc_Add_Item.Utilities.add_item_specific import update_create_free_text, CartItem, update_create_free_text_item
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import decrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients, get_currency_data, get_country_data
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Basic.Utilities.messages.messages import MSG016, MSG087
from eProc_Basic.decorators import authorize_view
from eProc_Configuration.models import Currency, UnitOfMeasures, FreeTextForm, ProductsDetail, ImagesUpload
from eProc_Exchange_Rates.Utilities.exchange_rates_generic import convert_currency
from eProc_Form_Builder.Utilities.form_builder_generic import FormBuilder, get_product_specification_details, \
    get_eform_update_price
from eProc_Form_Builder.models import EformFieldData
from eProc_Price_Calculator.Utilities.price_calculator_generic import calculate_total_value, calculate_item_total_value
from eProc_Shop_Home.models import RecentlyViewedProducts
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.free_text_form import CreateFreeText
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.limit_form import CreateLimitOrderForm
from eProc_Shopping_Cart.Shopping_Cart_Forms.call_off_forms.purchase_requisition_form import CreatePurchaseReqForm
from eProc_Shopping_Cart.Utilities.shopping_cart_generic import get_prod_cat, get_supplier_first_second_name
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import EditShoppingCart
from eProc_Shopping_Cart.Utilities.shopping_cart_specific import update_supplier_uom, update_supplier_desc, \
    update_unspsc, update_country
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_System_Settings.Utilities.system_settings_generic import sys_attributes

django_query_instance = DjangoQueries()

JsonParser_obj = JsonParser()


@login_required
@authorize_view(CONST_LIMIT_ORDER)
@transaction.atomic
def add_limit_item(request):
    """
    :param request: Get the form values from ui and saves the data to Database only if form is valid
    :return: limit_order.html after processing the request
    """
    update_user_info(request)
    client = getClients(request)
    product_category = get_prod_cat(request, prod_det=None)
    supplier_details = get_supplier_first_second_name(client)

    limit_form = CreateLimitOrderForm()
    context = {
        'inc_nav': True,
        'limit_form': limit_form,
        'product_category': product_category,
        'supplier_details': supplier_details,
        'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
        'is_slide_menu': True,
        'is_shop_active': True
    }

    return render(request, 'Add Item/limit_order.html', context)


#  Function to add  purchase requisition to cart
@login_required
@authorize_view(CONST_REQUISITION)
@transaction.atomic
def add_purch_req(request, document_number=None):
    """
    :param document_number:
    :param request: Get the form values from ui and saves the data to Database only if form is valid
    :return: purchase_requisition.html after processing the request
    """
    update_user_info(request)
    pr_form = CreatePurchaseReqForm()
    product_category = get_prod_cat(request, prod_det=None)
    if request.method == 'GET':
        if document_number != 'create':
            document_number = document_number.split('doc_number-')[1]
            document_number = decrypt(document_number)

    context = {
        'inc_nav': True,
        'shopping': True,
        'PRform': pr_form,
        'product_category': product_category,
        'unit': django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False}),
        'currency': django_query_instance.django_filter_only_query(Currency, {'del_ind': False}),
        'is_slide_menu': True,
        'document_number_decrypted': document_number,
        'is_shop_active': True
    }

    return render(request, 'Add Item/purchase_requisition.html', context)


# Function to define free text form based on supplier
# User story SP07-06
@login_required
@authorize_view(CONST_FREE_TEXT)
def free_text_form(request, encrypted_freetext_id, document_number):
    """
    :param document_number:
    :param request:
    :param supplier_id:
    :param product_category_id:
    :return:
    """
    update_user_info(request)
    client = global_variables.GLOBAL_CLIENT
    form_builder = FormBuilder()
    date_today = datetime.date.today()
    freetext_id = decrypt(encrypted_freetext_id)
    configured_free_text_form, eform_configured = form_builder.get_freetext_form(freetext_id)
    configured_free_text_form = update_unspsc(configured_free_text_form,'product_category_id')
    if document_number != 'create':
        document_number = decrypt(document_number.split('doc_number-')[1])
    context = {
        'inc_nav': True,
        'shopping': True,
        'free_text_form': CreateFreeText(),
        'unit': django_query_instance.django_filter_only_query(UnitOfMeasures, {'del_ind': False}),
        'is_slide_menu': True,
        'eform_configured': eform_configured,
        'configured_free_text_form': configured_free_text_form,
        'currency_list': get_currency_data(),
        'country_list': get_country_data(),
        'date_today': date_today,
        'decrypted_doc_number': document_number,
        'is_shop_active': True
    }

    return render(request, 'Add Item/free_text.html', context)


# Function to add freetext item to cart
@transaction.atomic
def add_free_text(request):
    if request.method == 'POST':
        update_user_info(request)
        # limit_item = check_for_limit(request)
        # if limit_item:
        #     return JsonResponse({'error': 'You cannot add other item with limit item'}, status=400)

        guid = guid_generator()
        free_text_fields = []
        eform = False
        data = JsonParser_obj.get_json_from_req(request)
        # eform_data = data['eform_data']
        # if data['eform_data']:
        #     eform = True
        #
        # item_name = request.POST.get('item_name')
        # prod_desc = request.POST.get('prod_desc')
        # price = request.POST.get('price')
        # uom = request.POST.get('uom')
        # del_date = request.POST.get('del_date')
        # quantity = request.POST.get('quantity')
        # supp_id = request.POST.get('supp_id')
        # product_category_id = request.POST.get('product_category_id')
        #
        # free_text_fields.append(eform)
        # free_text_fields.append(guid)
        # free_text_fields.append(item_name)
        # free_text_fields.append(prod_desc)
        # free_text_fields.append(price)
        # free_text_fields.append(uom)
        # free_text_fields.append(del_date)
        # free_text_fields.append(quantity)
        # free_text_fields.append(supp_id)
        #
        # if eform_data == 'eform':
        #     # Getting eform data
        #     form_field1 = request.POST.get('form_field1')
        #     form_field2 = request.POST.get('form_field2')
        #     form_field3 = request.POST.get('form_field3')
        #     form_field4 = request.POST.get('form_field4')
        #     form_field5 = request.POST.get('form_field5')
        #     form_field6 = request.POST.get('form_field6')
        #     form_field7 = request.POST.get('form_field7')
        #     form_field8 = request.POST.get('form_field8')
        #     form_field9 = request.POST.get('form_field9')
        #     form_field10 = request.POST.get('form_field10')
        #     form_id = django_query_instance.django_get_query(FreeTextForm, {'supp_id': supp_id,
        #                                                                     'prod_cat_id': product_category_id,
        #                                                                     'client': getClients(request)})
        #
        #     # Appending eform data
        #     free_text_fields.append(form_field1)
        #     free_text_fields.append(form_field2)
        #     free_text_fields.append(form_field3)
        #     free_text_fields.append(form_field4)
        #     free_text_fields.append(form_field5)
        #     free_text_fields.append(form_field6)
        #     free_text_fields.append(form_field7)
        #     free_text_fields.append(form_field8)
        #     free_text_fields.append(form_field9)
        #     free_text_fields.append(form_field10)
        #     free_text_fields.append(form_id)
        is_saved = update_create_free_text_item(data)
        if not is_saved[0]:
            return JsonResponse({'error': is_saved[1]}, status=400)
        else:
            return JsonResponse({'success': MSG016})


def update_or_create_item(request, document_number=None):
    update_user_info(request)
    if request.is_ajax():
        edit_object = EditShoppingCart(request)
        item_details = JsonParser().get_json_from_req(request)
        selected_currency = None

        if 'currency' in item_details:
            selected_currency = item_details['currency']

        username = global_variables.GLOBAL_LOGIN_USERNAME
        user_currency = request.user.currency_id
        cart_item_instance = CartItem(username, user_currency, selected_currency)

        client_li = getClients(request)
        sys_attributes_instance = sys_attributes(client_li)
        limit_item_flag = sys_attributes_instance.get_limit_item()

        if limit_item_flag == '0':
            if 'guid' not in item_details:
                if cart_item_instance.limit_order_validation(item_details['call_off']):
                    return JsonResponse({'error': MSG087}, status=400)

        if item_details['call_off'] == CONST_CO04:
            guid, updated_item_details = cart_item_instance.update_item_details_for_limit(item_details)
            cart_item_instance.add_or_update_item(guid, updated_item_details)

            if 'guid' in item_details:
                item_value = convert_currency(item_details['overall_limit'],
                                              str(selected_currency), str(user_currency))
                if not item_value:
                    return JsonResponse({'error_message': f'Invalid Currency {selected_currency}'}, status=401)

                return JsonResponse({'item_value': item_value}, status=201)

        if item_details['call_off'] == CONST_CO03:
            guid, updated_item_details, item_value = cart_item_instance.update_item_details_for_pr(
                item_details, document_number, edit_object)

            if document_number == 'create':
                cart_item_instance.add_or_update_item(guid, updated_item_details)

                if 'guid' in item_details:
                    return JsonResponse({'item_value': item_value, 'total_value': calculate_total_value(username)})

        if item_details['call_off'] == CONST_CO02:
            if document_number != 'create':
                guid, eform_data, updated_item_details, item_value, form_id = cart_item_instance \
                    .update_item_details_for_freetext(item_details, document_number, edit_object)

            if document_number == 'create':
                item_detail = item_details['cart_item_data']
                cart_item_instance.add_or_update_item(item_detail['guid'], item_detail)
                item_value = calculate_item_total_value(CONST_CO02, item_detail['quantity'], None, 1,
                                                        item_detail['price'], overall_limit=None)
                # update free text eform data
                save_eform_data(item_details['eform_data'])
            return JsonResponse({'item_value': item_value, 'total_value': calculate_total_value(username)})

            # if eform_data == 'eform':
            #     cart_item_instance.update_eform_details(guid, JsonParser().get_json_from_req(request), form_id)

            # if 'guid' in item_details:
            #     return JsonResponse({'item_value': item_value, 'total_value': calculate_total_value(username)})

        if item_details['call_off'] == CONST_CO01:
            product_id = item_details['prod_id']
            quantity = item_details['quantity']
            document_number = item_details['document_number']
            res = cart_item_instance.add_catalog_item(product_id, edit_object, document_number, username, quantity,
                                                      item_details)
            if res[0]:
                if document_number == 'create':
                    return JsonResponse({'res': res[1], 'cart_count': res[2]})
                else:
                    return JsonResponse({'res': res[1]})
            else:
                return JsonResponse({'error': res[1]})

    return JsonResponse({'success': MSG016})


def save_eform_data(eform_data):
    """

    """
    for eform_detail in eform_data:
        django_query_instance.django_update_query(EformFieldData,
                                                  {'eform_field_data_guid': eform_detail['eform_transaction_guid']},
                                                  {'eform_field_data': eform_detail['eform_data']})

def get_product_service_product_details(request, product_id):
    """

    :param request:
    :return:
    """
    update_user_info(request)
    eform_detail = []
    product_specification = []
    quantity_dictionary = []
    item_price = None
    username = global_variables.GLOBAL_LOGIN_USERNAME
    client = global_variables.GLOBAL_CLIENT
    product_details = {}
    prod_id = product_id
    # catalog_id = catalog_id
    prod_detail = {}
    context = {
        'inc_nav': True,
        'inc_footer': True,
    }
    if django_query_instance.django_existence_check(ProductsDetail, {'client': global_variables.GLOBAL_CLIENT,
                                                                     'product_id': prod_id}):
        prod_detail = django_query_instance.django_filter_query(ProductsDetail,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'product_id': prod_id}, None, None)[0]
        prod_detail_get_query = django_query_instance.django_get_query(ProductsDetail,
                                                                       {'client': global_variables.GLOBAL_CLIENT,
                                                                        'product_id': prod_id})
        if prod_detail:
            prod_detail = update_supplier_uom(prod_detail)
            prod_detail = update_unspsc(prod_detail,'prod_cat_id_id')
            prod_detail = update_country(prod_detail)

        if prod_detail_get_query.eform_id:
            eform_detail, item_price, quantity_dictionary = get_eform_update_price(prod_detail_get_query.eform_id)

            for data in eform_detail:
                data['eform_field_data'] = data['eform_field_data'].split('|~#')

        if prod_detail_get_query.product_info_id:
            product_specification = get_product_specification_details(prod_detail_get_query.product_info_id)
        if item_price:
            prod_detail['price'] = item_price

    context['prod_detail'] = prod_detail

    prod_img_detail = django_query_instance.django_filter_query(ImagesUpload,
                                                                {'client': global_variables.GLOBAL_CLIENT,
                                                                 'image_id': prod_id,
                                                                 'image_type': CONST_CATALOG_IMAGE_TYPE
                                                                 }, None, None)

    # Add to recently viewed products
    existing_product_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'product_id': prod_id,
        'username': username,
        'client': client,
        'del_ind': False
    })
    if not existing_product_query.exists():
        django_query_instance.django_create_query(RecentlyViewedProducts, {
            'recently_viewed_prod_guid': guid_generator(),
            'client': global_variables.GLOBAL_CLIENT,
            'username': global_variables.GLOBAL_LOGIN_USERNAME,
            'product_id': prod_detail['product_id'],
            'catalog_id': prod_detail['prod_cat_id_id'],
            'recently_viewed_prod_created_at': datetime.datetime.now(),
            'recently_viewed_prod_created_by': global_variables.GLOBAL_LOGIN_USERNAME,
            'del_ind': False
        })

    recently_viewed_products_query = django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
        'username': username,
        'client': client,
        'del_ind': False
    })

    context['prod_img_detail'] = prod_img_detail
    context['eform_detail'] = eform_detail
    context['quantity_dictionary'] = quantity_dictionary
    context['product_specification'] = product_specification
    if existing_product_query.exists():
        existing_product_query.update(recently_viewed_prod_changed_at=datetime.datetime.now(),
                                      recently_viewed_prod_changed_by=username)
        print(context)
        return render(request, 'Product_Details_Page/product_detail_page.html', context)

    if recently_viewed_products_query.count() == CONST_USER_RECENTLY_VIEWED:
        django_query_instance.django_filter_only_query(RecentlyViewedProducts, {
            'username': username,
            'client': client,
            'del_ind': False
        }).earliest('recently_viewed_prod_created_at').delete()

    guid = guid_generator()
    # django_query_instance.django_update_or_create_query(RecentlyViewedProducts, {'recently_viewed_prod_guid': guid}, {
    #     'username': username,
    #     'product_id': prod_id,
    #     'catalog_id': catalog_id,
    #     'recently_viewed_prod_created_at': datetime.datetime.now(),
    #     'recently_viewed_prod_created_by': username,
    #     'recently_viewed_prod_changed_at': datetime.datetime.now(),
    #     'recently_viewed_prod_changed_by': username,
    #     'client_id': client,
    # })
    print(context)
    return render(request, 'Product_Details_Page/product_detail_page.html', context)