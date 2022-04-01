from django.urls import path
from . import views

app_name = 'eProc_Application_Settings'

urlpatterns = [
    path('get_number_ranges/', views.get_number_ranges, name='get_number_ranges'),
    path('clients/', views.upload_clients, name='upload_clients'),
    path('UNSPSC_codes/', views.upload_product_category, name='upload_product_category'),
    path('org_node_types', views.org_node_types, name='org_node_types'),
    path('document_types/', views.upload_document_type, name='upload_document_type'),
    path('sc_number_ranges/', views.number_range_shopping_cart, name='number_range_shopping_cart'),
    path('po_number_ranges/', views.number_range_purchase_order, name='number_range_purchase_order'),
    path('confirmation_number_ranges/', views.number_range_goods_verification,
         name='number_range_goods_verification'),
    path('roles', views.roles, name='roles'),
    path('authorization_objects', views.auth_objects, name='auth_objects'),
    path('authorization_grp', views.auth_grp, name='auth_grp'),
    path('org_attributes', views.org_attributes, name='org_attributes'),
    path('authorization', views.auth, name='auth'),
    path('favourite_transaction_types/', views.transaction_type, name='transaction_type'),
    path('sc_transaction_types/', views.transaction_type_sc, name='transaction_type_sc'),
    path('po_transaction_types/', views.transaction_type_po, name='transaction_type_po'),
    path('gv_transaction_types/', views.transaction_type_gv, name='transaction_type_gv'),
    path('ACC/', views.upload_acc_assign_categories, name='upload_acc_assign_categories'),
    path('calendars', views.display_calendar, name='display_calendar'),
    path('holidays', views.display_holidays, name='display_holidays'),
    path('message_numbers/', views.display_messages_id, name='display_messages_id'),
    path('message_descriptions/', views.display_messages_desc, name='display_messages_desc'),
    path('edit_create_number_ranges/', views.edit_create_number_ranges, name='edit_create_number_ranges'),
    path('get_transaction_type/', views.get_transaction_type, name='get_transaction_type'),
    path('edit_create_transaction_types/', views.edit_create_transaction_types, name='edit_create_transaction_types'),
    path('purch_cockpit', views.purch_cockpit_display, name='purch_cockpit'),
    path('save_purch_cockpit', views.save_purch_cockpit_data, name='save_purch_cockpit'),
    path('save_product_details_images', views.save_product_details_images, name='save_product_details_images'),

]
