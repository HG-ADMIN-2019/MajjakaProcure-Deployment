from django.http import HttpResponse
from django.shortcuts import render

from eProc_Generate_PDF.views import render_pdf_view


def view_purchase_order(request):

    context = {
        'inc_nav': True,
        'is_slide_menu': True,
    }

    return render(request, 'purchase_order/purchase_order.html', context)


# def generate_sc_details_pdf(request):
#     pdf = render_pdf_view('sc_pdf.html')
#
#     return HttpResponse(pdf, content_type='application/pdf')