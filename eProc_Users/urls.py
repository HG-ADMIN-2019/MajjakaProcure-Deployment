from django.urls import path
from .views import *


app_name = 'eProc_Users'

urlpatterns = [
    path('register_user/', register_page, name='register_page'),
    path('update_user_basic_details/', update_user_basic_details, name='update_user_basic_details'),
]
