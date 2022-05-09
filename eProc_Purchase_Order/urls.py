from django.urls import path

from . import views

app_name = 'eProc_Purchase_Order'

urlpatterns = [
    path('', views.view_purchase_order, name='view_purchase_order'),
]