import os
import uuid
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings

from eProc_Basic.Utilities.global_defination import global_variables


def save_pdf(params: dict):
    """

    """
    template = get_template("po_pdf_mockup.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = str(params['doc_number'])
    path =str(settings.BASE_DIR) + f'/media/po_pdf/{global_variables.GLOBAL_CLIENT}/{file_name}.pdf'
    count = 1
    while os.path.exists(path):
        path = str(settings.BASE_DIR) + f'/media/po_pdf/{global_variables.GLOBAL_CLIENT}/{file_name}-{count}.pdf'
        count = count+1
    try:
        with open(path, 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)
    if pdf.error:
        return '', False,path

    return file_name, True,path
