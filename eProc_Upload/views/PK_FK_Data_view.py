from django.contrib.auth.decorators import login_required
import csv
import io

from django.shortcuts import render
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError

from eProc_Upload.Utilities.upload_data.upload_basic_pk_fk_tables import UploadPkFkTables


def UploadPkFkData(request, app_name, table_name):
    if request.method == 'POST':
        Test_mode = request.POST.get('test')
        try:
            csv_file = request.FILES['file']
            data = csv.DictReader(request.FILES['file'])
            print(data)
            if not csv_file.name.endswith('.csv'):
                messages.error(request, MSG044)
                return render(request, "Upload/upload_csv_attachment.html")
            data_set = csv_file.read().decode('utf8')

            fin_upld_data = io.StringIO(data_set)
            final_save = UploadPkFkTables()
            final_save.header_data = fin_upld_data
            final_save.app_name = app_name
            final_save.table_name = table_name
            final_save.test_mode = Test_mode
            final_save.request = request

            is_save = final_save.guids_table_conditions()

        except MultiValueDictKeyError:
            csv_file = False
            messages.error(request, MSG048)
    return render(request, "Upload/upload_csv_attachment.html")

