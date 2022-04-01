from django.urls import path
from .views import *

app_name = 'eProc_Basic_Settings'

urlpatterns = [
    path('export', extract_country_data, name='extract_country_data'),
    path('extract_country_template', extract_country_template, name='extract_country_template'),
    path('export_product_category', extract_product_category_data, name='extract_product_category_data'),
    path('export_languages', extract_language_data, name='extract_language_data'),
    path('extract_language_template', extract_language_template, name='extract_language_template'),
    path('export_currency', extract_currency_data, name='extract_currency_data'),
    path('export_timezone_data', extract_timezone_data, name='extract_timezone_data'),
    path('extract_timezone_template', extract_timezone_template, name='extract_timezone_template'),
    path('export_unitofmeasure', extract_unitofmeasure_data, name='extract_unitofmeasure_data'),
    path('extract_unitofmeasure_template', extract_unitofmeasure_template, name='extract_unitofmeasure_template'),
    path('export_product_details', extract_product_details, name='extract_product_details'),
    path('export_emp', extract_employee_data, name='extract_employee_data'),
    path('countries/', upload_countries, name='upload_countries'),
    path('data_upload/', data_upload, name='data_upload'),
    path('check_data/', check_data, name='check_data'),
    path('currencies/', upload_currencies, name='upload_currencies'),
    path('languages/', upload_languages, name='upload_languages'),
    path('timezones/', upload_timezone, name='upload_timezone'),
    path('unit_of_measures/', upload_unit_of_measure, name='upload_unit_of_measure'),
    path('upload_data_display', upload_data_display, name='upload_data_display'),
    path('ACC_values', account_ass_values, name='account_ass_values'),
    path('purch_Cockpit', purch_Cockpit, name='purch_Cockpit'),
    path('save_basic_data', save_basic_data, name='save_basic_data'),
    path('create_update_basic_data', create_update_basic_data, name='create_update_basic_data'),

]
