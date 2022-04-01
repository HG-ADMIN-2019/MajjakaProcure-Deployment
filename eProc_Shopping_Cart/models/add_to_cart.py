from django.db import models


# Defining model field for storing cart item details
# User-story SC-LO-US01
class CartItemDetails(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32, null=False, default=None)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=True, verbose_name='Item Number')
    description = models.CharField(db_column='DESCRIPTION', max_length=250, null=True)
    long_desc = models.CharField(db_column='LONG_DESC', max_length=3000, blank=True, null=True,
                                 verbose_name='Product Long desc')
    prod_cat_desc = models.CharField(db_column='PROD_CAT_DESC', max_length=255, blank=False, null=True,
                                     verbose_name='Product Category Description')
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, null=True)
    int_product_id = models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)
    ext_product_id = models.PositiveIntegerField(db_column='EXT_PRODUCT_ID', null=True, blank=True)
    quantity = models.CharField(db_column='QUANTITY', max_length=20, null=True)
    unit = models.CharField(db_column='UNIT', max_length=30, null=True)
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, null=True)
    gross_price = models.DecimalField(db_column='GROSS_PRICE', max_digits=13, decimal_places=2, null=True)
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, null=True)
    currency = models.CharField(db_column='CURRENCY', max_length=3, null=True)
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=10, null=True)
    pref_supplier = models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True)
    lead_time = models.PositiveIntegerField(db_column='LEAD_TIME', null=True)
    value = models.CharField(db_column='VALUE', max_length=20, null=True)
    supp_txt = models.CharField(db_column='SUPP_TXT', max_length=1000, blank=True, null=True,
                                verbose_name='Supplier Text')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, null=True)
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, null=True)
    supp_prod_num = models.CharField(db_column='SUPP_PROD_NUM', max_length=40, null=True)
    call_off = models.CharField(db_column='CALL_OFF', max_length=15, null=True)
    supplier_contact = models.CharField(max_length=40, db_column='SUPPLIER_CONTACT', blank=True, null=True)
    supplier_fax_no = models.CharField(max_length=30, db_column='SUPPLIER_FAX_NO', blank=True, null=True)
    supplier_email = models.CharField(max_length=100, db_column='SUPPLIER_EMAIL', blank=True, null=True)
    quantity_min = models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True)
    value_min = models.PositiveIntegerField(db_column='VALUE_MIN', null=True)
    tiered_flag = models.BooleanField(db_column='TIERED_FLAG', null=True)
    bundle_flag = models.BooleanField(db_column='BUNDLE_FLAG', null=True)
    tax_code = models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')
    delivery_days = models.DateField(db_column='DELIVERY_DAYS', null=True)
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, null=True)
    catalog_item = models.CharField(db_column='CATALOG_ITEM', max_length=32, null=True)
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, null=True)
    contract = models.CharField(db_column='contract', max_length=50, null=True)
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, null=True)
    item_del_date = models.DateField(db_column='ITEM_DEL_DATE', blank=False, null=True)
    process_type = models.CharField(db_column='PROCESS_TYPE', max_length=8, null=True)
    start_date = models.DateField(db_column='START_DATE', null=True)
    end_date = models.DateField(db_column='END_DATE', null=True)
    ir_gr_ind = models.BooleanField(db_column='IR_GR_IND', null=True)
    gr_ind = models.BooleanField(db_column='GR_IND', null=True, verbose_name='Gr ind')
    overall_limit = models.DecimalField(db_column='OVERALL_LIMIT', max_digits=15, decimal_places=2, null=True)
    expected_value = models.DecimalField(db_column='EXPECTED_VALUE', max_digits=15, decimal_places=2, null=True)
    username = models.CharField(db_column='USERNAME', max_length=16, null=False)
    cart_item_requested_by = models.CharField(db_column='CART_ITEM_REQUESTED_BY', max_length=30, null=True)
    cart_item_created_at = models.DateTimeField(db_column='CART_ITEM_CREATED_AT', blank=True, null=True)
    cart_item_created_by = models.CharField(db_column='CART_ITEM_CREATED_BY', max_length=30, null=True)
    cart_item_changed_at = models.DateTimeField(db_column='CART_ITEM_CHANGED_AT', blank=True, null=True)
    cart_item_changed_by = models.CharField(db_column='CART_ITEM_CHANGED_BY', max_length=30, null=True)
    cart_item_details_source_system = models.CharField(db_column='CART_ITEM_DETAILS_SOURCE_SYSTEM', max_length=20)
    cart_item_details_destination_system = models.CharField(db_column='CART_ITEM_DETAILS_DESTINATION_SYSTEM',
                                                            max_length=20)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        db_table = 'MTD_CART_ITEM'
