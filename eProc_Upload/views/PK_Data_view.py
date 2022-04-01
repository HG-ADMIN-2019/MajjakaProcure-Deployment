from django.contrib.auth.decorators import login_required
import csv
import io

from django.shortcuts import render
from django.contrib import messages
from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError

from eProc_Upload.Utilities.upload_data.upload_pk_tables import UploadBasicTables


@login_required
def data_upload(req):
    """
    on click of Data upload in nav bar liked to data upload page
    :param req: request data from UI
    :return: render data_upload.html and context
    """
    context = {'inc_nav': True, 'nav_title': 'Upload data'}
    return render(req, 'Upload/data_upload.html', context)


def UploadPKData(request, app_name, table_name):
    if request.method == 'POST':
        test_mode = request.POST.get('test')
        try:
            csv_file = request.FILES['file']
            data = csv.DictReader(request.FILES['file'])
            if not csv_file.name.endswith('.csv'):
                messages.error(request, MSG044)
                return render(request, "Upload/upload_csv_attachment.html")
            data_set = csv_file.read().decode('utf8')

            fin_upld_data = io.StringIO(data_set)
            final_save = UploadBasicTables(request)
            final_save.header_data = fin_upld_data
            final_save.app_name = app_name
            final_save.table_name = table_name
            final_save.test_mode = test_mode
            final_save.request = request

            is_saved = final_save.basic_table_conditions()

        except MultiValueDictKeyError:
            csv_file = False
            messages.error(request, MSG048)
    return render(request, "Upload/upload_csv_attachment.html")

