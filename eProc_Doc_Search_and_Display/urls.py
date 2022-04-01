from django.urls import path
from . import views

app_name = 'eProc_Doc_Search_and_Display'

urlpatterns = [
    path('sc_completion_doc_search/', views.sc_completion_doc_search, name='sc_completion_doc_search'),
    path('get_sc_for_approval/', views.get_sc_for_approval, name='get_sc_for_approval'),
    path('search_shopping_carts', views.sc_po_hdr_search, name='search_shopping_carts'),
]
