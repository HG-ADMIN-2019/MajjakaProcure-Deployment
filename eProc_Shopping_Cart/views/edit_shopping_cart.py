from django.db import transaction
from django.http.response import JsonResponse
from eProc_Shopping_Cart.Utilities.save_order_edit_sc import EditShoppingCart


@transaction.atomic
def edit_saved_shopping_cart(request):
    edit_sc = EditShoppingCart(request)
    if 'delete_sc' in request.POST:
        header_guid = request.POST.get('header_guid')
        edit_sc.delete_sc(header_guid)
        return JsonResponse({'message': ''})
    else:
        del_item_guid = request.POST.get('del_item_guid')
        total_value = request.POST.get('total_value')
        header_guid = request.POST.get('header_guid')
        delete_info = edit_sc.delete_item_from_sc(del_item_guid, total_value, header_guid)
        return JsonResponse({'total_value': delete_info[0], 'count': delete_info[1]})
