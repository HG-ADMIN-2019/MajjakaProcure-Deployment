from django.urls import path
from . import views

# User story : SE10-15 - Admin Tools

# defines the app name sets the URL's to call the respective function
from .views import delete_user, lock_unlock_emp, get_username

app_name = 'eProc_Admin_Tool'

urlpatterns = [
    path('', views.admin_tool, name='admin_tool'),
    path('employee_management/', views.user_search, name='employee_search'),
    path('delete_user/', delete_user, name='delete_user'),
    path('lock_unlock_emp/', lock_unlock_emp, name='lock_unlock_emp'),
    path('get_username/', get_username, name='get_username'),
    path('supplier_management/', views.supplier_search, name='supplier_search'),
    path('employee_management/user_details/<str:email>/', views.user_details, name='user_details_page'),
    path('supplier_management/supplier_details/<str:supplier_id>/', views.sup_details, name='sup_details_page'),
    path('admin_report/users', views.user_report, name='user_report'),  # reports_main page
    path('admin_report/approvals', views.approval_report, name='approval_report'),  # approval report_main page
    path('admin_report/documents', views.m_docsearch_meth, name='doc_search_report'),  # Search page
    path('admin_report/account_assignment_categories',views.accnt_report, name='accnt_report') , # accounting report_main page
    path('bulletin_configuration/', views.org_announcements_search, name='org_announcements_search'),
    path('bulletin_details/<str:announcement_guid>/', views.org_announcement_details, name='org_announcement_details'),
    path('extract_employee_template', views.extract_employee_template, name='extract_employee_template'),

]
