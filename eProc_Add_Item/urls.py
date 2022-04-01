from django.urls import path
from . import views

app_name = 'eProc_Add_Item'

urlpatterns = [
    path('limit_form', views.add_limit_item, name='limit_form'),
    path('purchase_requisition/<str:document_number>', views.add_purch_req, name='purchreq'),
    path('free_text/<str:encrypted_freetext_id>/<str:document_number>', views.free_text_form,
         name='freetext'),
    path('add_free_text/', views.add_free_text, name='add_free_text'),
    path('update_or_create_item/<str:document_number>', views.update_or_create_item, name='update_or_create_item')
]
