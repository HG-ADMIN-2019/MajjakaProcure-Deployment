from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Form_Builder.models import EformData, EformFieldData
from eProc_Notes_Attachments.models import Attachments, Notes
from eProc_Purchase_Order.models import PoHeader, PoItem, PoAccounting, PoAddresses, PoApproval, PoPotentialApproval
from eProc_Shopping_Cart.models import ScItem, PurchasingData, ScAccounting, ScAddresses, ScApproval, ScHeader, \
    ScPotentialApproval, PurchasingUser

django_query_instance = DjangoQueries()


def delete_all_shopping_carts(filter_criteria, client):
    delete_po_data(filter_criteria,client)
    sc_header_guid_list = django_query_instance.django_filter_value_list_query(ScHeader, filter_criteria, 'guid')
    for header_guid in sc_header_guid_list:
        item_guid_list = django_query_instance.django_filter_value_list_query(ScItem,
                                                                              {'header_guid': header_guid,
                                                                               'client': client}, 'guid')

        for item_guid in item_guid_list:
            django_query_instance.django_filter_delete_query(PurchasingUser, {'sc_item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_filter_delete_query(PurchasingData, {'sc_item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_filter_delete_query(Attachments, {'item_guid': item_guid,
                                                                           'client': client})

            django_query_instance.django_filter_delete_query(Notes, {'item_guid': item_guid,
                                                                     'client': client})

            django_query_instance.django_filter_delete_query(ScAccounting, {'item_guid': item_guid,
                                                                            'client': client})

            django_query_instance.django_filter_delete_query(ScAddresses, {'item_guid': item_guid,
                                                                           'client': client})

            django_query_instance.django_filter_delete_query(EformFieldData, {'item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_filter_delete_query(ScItem, {'guid': item_guid,
                                                                      'client': client})

        hdr_guid = django_query_instance.django_filter_only_query(ScApproval,
                                                                  {'header_guid': header_guid, 'client': client})
        for approval in hdr_guid:
            django_query_instance.django_filter_delete_query(ScPotentialApproval, {'sc_header_guid': header_guid})
            django_query_instance.django_filter_delete_query(ScApproval, {'header_guid': approval.guid,
                                                                          'client': client})
        django_query_instance.django_filter_delete_query(PurchasingUser, {'sc_header_guid': header_guid,
                                                                          'client': client})
        django_query_instance.django_filter_delete_query(ScPotentialApproval, {'sc_header_guid': header_guid})
        django_query_instance.django_filter_delete_query(ScApproval, {'header_guid': header_guid})
        django_query_instance.django_filter_delete_query(ScAccounting, {'header_guid': header_guid})
        django_query_instance.django_filter_delete_query(ScAddresses, {'header_guid': header_guid})
        django_query_instance.django_filter_delete_query(ScHeader, {'guid': header_guid, 'client': client})


def delete_po_data(filter_criteria,client):
    """

    """
    sc_header_guid_list = django_query_instance.django_filter_value_list_query(PoHeader, filter_criteria, 'po_header_guid')
    for header_guid in sc_header_guid_list:
        item_guid_list = django_query_instance.django_filter_value_list_query(PoItem,
                                                                              {'po_header_guid': header_guid,
                                                                               'client': client}, 'po_item_guid')

        for item_guid in item_guid_list:
            django_query_instance.django_filter_delete_query(PurchasingUser, {'po_item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_filter_delete_query(PurchasingData, {'po_item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_filter_delete_query(Attachments, {'item_guid': item_guid,
                                                                           'client': client})

            django_query_instance.django_filter_delete_query(Notes, {'item_guid': item_guid,
                                                                     'client': client})

            django_query_instance.django_filter_delete_query(PoAccounting, {'po_item_guid': item_guid,
                                                                            'client': client})

            django_query_instance.django_filter_delete_query(PoAddresses, {'po_item_guid': item_guid,
                                                                           'client': client})

            django_query_instance.django_filter_delete_query(EformFieldData, {'po_item_guid': item_guid,
                                                                              'client': client})

            django_query_instance.django_update_query(ScItem,{'po_item_guid': item_guid,
                                                                      'client': client},
                                                      {'po_item_guid':None})

            django_query_instance.django_filter_delete_query(PoItem, {'po_item_guid': item_guid,
                                                                      'client': client})

        hdr_guid = django_query_instance.django_filter_only_query(PoApproval,
                                                                  {'po_header_guid': header_guid, 'client': client})
        for approval in hdr_guid:
            django_query_instance.django_filter_delete_query(PoPotentialApproval, {'po_header_guid': header_guid})
            django_query_instance.django_filter_delete_query(PoApproval, {'po_header_guid': approval.po_header_guid,
                                                                          'client': client})
        django_query_instance.django_filter_delete_query(PurchasingUser, {'po_header_guid': header_guid,
                                                                          'client': client})
        django_query_instance.django_filter_delete_query(PoPotentialApproval, {'po_header_guid': header_guid})
        django_query_instance.django_filter_delete_query(PoApproval, {'po_header_guid': header_guid})
        django_query_instance.django_filter_delete_query(PoAccounting, {'po_header_guid': header_guid})
        django_query_instance.django_filter_delete_query(PoAddresses, {'po_header_guid': header_guid})
        django_query_instance.django_filter_delete_query(PoHeader, {'po_header_guid': header_guid, 'client': client})

