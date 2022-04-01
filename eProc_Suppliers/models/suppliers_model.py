from django.db import models


class OrgSuppliers(models.Model):
    guid = models.CharField(primary_key=True, db_column='GUID', max_length=32, default=None)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, verbose_name='Vendor Id', null=True)
    sup_address_number = models.PositiveIntegerField(db_column='SUP_ADDRESS_NUMBER', null=True)
    porg_object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                       null=True,
                                       default=None)
    payment_term_key = models.CharField(db_column='PAYTERM_KEY', blank=True, null=True, max_length=4,
                                        verbose_name='Payment Term')
    incoterm_key = models.ForeignKey('eProc_Configuration.Incoterms', models.DO_NOTHING, db_column='INCOTERM_KEY',
                                     blank=True, null=True, verbose_name='Incoterm1')
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY', null=True)
    gr_inv_vrf = models.BooleanField(db_column='GR_INVOICE_VERIFICATION', default=False, null=False)
    inv_conf_exp = models.BooleanField(db_column='INVOICE_CONFIRMATION_EXPECTED', default=False, null=False)
    gr_conf_exp = models.BooleanField(db_column='GR_CONFIRMATION_EXPECTED', default=False, null=False)
    po_resp = models.BooleanField(db_column='PO_RESPONSE', default=False, null=False)
    ship_notif_exp = models.BooleanField(db_column='SHIPPING_NOTIF_EXPECTED', default=False, null=False)
    purch_block = models.BooleanField(db_column='PURCHASE_BLOCK', default=False, null=False)
    porg_id = models.CharField(db_column='P_ORG_ID', max_length=8)
    org_supp_created_at = models.DateTimeField(db_column='ORG_SUPP_CREATED_AT', blank=True, null=True)
    org_supp_created_by = models.CharField(db_column='ORG_SUPP_CREATED_BY', max_length=30, null=True)
    org_supp_changed_at = models.DateTimeField(db_column='ORG_SUPP_CHANGED_AT', blank=True, null=True)
    org_supp_changed_by = models.CharField(db_column='ORG_SUPP_CHANGED_BY', max_length=30, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_ORG_SUPPLIERS'
