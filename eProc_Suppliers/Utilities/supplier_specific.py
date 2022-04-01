from eProc_Suppliers.Utilities.supplier_generic import Supplier


def get_sup_list_by_input(request):
    supplier_instance = Supplier()
    inp_supp_id = request.POST.get('supplier_id')
    inp_srch1 = request.POST.get('search_term1')
    inp_srch2 = request.POST.get('search_term2')
    inp_first_name = request.POST.get('first_name')
    inp_last_name = request.POST.get('last_name')
    inp_country = request.POST.get('country')
    inp_city = request.POST.get('city')

    args_list = {}

    if inp_supp_id is not None and inp_supp_id != '':
        args_list['supplier_id'] = inp_supp_id

    if inp_srch1 is not None and inp_srch1 != '':
        args_list['search_term1'] = inp_srch1

    if inp_srch2 is not None and inp_srch2 != '':
        args_list['search_term2'] = inp_srch2

    if inp_first_name is not None and inp_first_name != '':
        args_list['name1'] = inp_first_name

    if inp_last_name is not None and inp_last_name != '':
        args_list['name2'] = inp_last_name

    if inp_country is not None and inp_country != '':
        args_list['country_code'] = inp_country

    if inp_city is not None and inp_city != '':
        args_list['city'] = inp_city

    result = supplier_instance.filter_supplier_query(args_list)

    return result

