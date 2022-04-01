from django.urls import path
from .views import *

app_name = 'eProc_Emails'

urlpatterns = [
    path('eProc_Email_Notification/', email_notification_form, name='email_notif'),
    path('eProc_Email_Notification_Edit/', edit_email_notif_form, name='edit_email_notif_form'),
    path('eProc_Email_Notification_Update/', update_email_notif_form, name='update_email_notif_form'),
]
# eProc_Email_Notification:update_email_notif_form
# eProc_Emails:update_email_notif_form
