from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'eProc_Shopping_Cart'

urlpatterns = [
    path('create_shopping_cart/', views.sc_first_step, name='cart-details'),
    path('update_item/', views.update_item, name='update_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('eform_data/', views.display_eform_data, name='eform_data'),
    path('empty_shopping_cart/', views.empty_shopping_cart, name='empty'),
    path('review_shopping_cart/', views.review_page, name='review_sc'),
    path('save_shopping_cart/', views.save_shopping_cart, name='save_sc'),
    path('change_ship_adr/', views.change_ship_adr, name='change_ship_adr'),
    path('update_free_text_item/', views.update_free_text_item, name='update_free_text_item'),
    path('check_shopping_cart/', views.check_shopping_cart, name='check_shopping_cart'),
    path('edit_shopping_cart/', views.edit_saved_shopping_cart, name='edit_saved_shopping_cart'),
    path('order_shopping_cart/', views.order_shopping_cart, name='order_shopping_cart'),
    path('update_quantity', views.update_quantity, name='update_quantity'),
    path('auto_complete_goods_receiver', views.auto_complete_goods_receiver, name='auto_complete_goods_receiver'),
    path('update_catalog_item/', views.update_catalog_item, name='update_catalog_item'),
    path('update_user_name', views.update_user_name, name='update_user_name'),
    path('ajax_trigger_wf', views.ajax_trigger_wf, name='ajax_trigger_wf'),
]

# Start of SC-PR-US13
# These lines of code creates dynamic url for attachments

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# End of SC-PR-US13
