import os
from django.db import models
from eProc_Configuration.models import OrgClients


class EformData(models.Model):
    cart_guid = models.CharField(db_column='CART_GUID', primary_key=True, max_length=32, null=False)
    form_field1 = models.CharField(db_column='FORM_FIELD1', blank=True, null=True, max_length=50)
    form_field2 = models.CharField(db_column='FORM_FIELD2', blank=True, null=True, max_length=50)
    form_field3 = models.CharField(db_column='FORM_FIELD3', blank=True, null=True, max_length=50)
    form_field4 = models.CharField(db_column='FORM_FIELD4', blank=True, null=True, max_length=50)
    form_field5 = models.CharField(db_column='FORM_FIELD5', blank=True, null=True, max_length=50)
    form_field6 = models.CharField(db_column='FORM_FIELD6', blank=True, null=True, max_length=50)
    form_field7 = models.CharField(db_column='FORM_FIELD7', blank=True, null=True, max_length=50)
    form_field8 = models.CharField(db_column='FORM_FIELD8', blank=True, null=True, max_length=50)
    form_field9 = models.CharField(db_column='FORM_FIELD9', blank=True, null=True, max_length=50)
    form_field10 = models.CharField(db_column='FORM_FIELD10', blank=True, null=True, max_length=50)
    item_num = models.PositiveIntegerField(db_column='ITEM_NUM', blank=False, null=True, verbose_name='Item Number')
    eform_data_created_at = models.DateTimeField(db_column='EFORM_DATA_CREATED_AT', blank=False, null=True)
    eform_data_created_by = models.CharField(db_column='EFORM_DATA_CREATED_BY', max_length=12, blank=False, null=True)
    eform_data_changed_at = models.DateTimeField(db_column='EFORM_DATA_CHANGED_AT', blank=True, null=True)
    eform_data_changed_by = models.CharField(db_column='EFORM_DATA_CHANGED_BY', max_length=12, blank=False, null=True)
    eform_data_source_system = models.CharField(db_column='eform_data_source_system', max_length=20)
    eform_data_destination_system = models.CharField(db_column='EFORM_DATA_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='ITEM_GUID', null=True)
    form_id = models.ForeignKey('eProc_Configuration.FreeTextForm', models.DO_NOTHING, db_column='FORM_ID')

    def __str__(self):
        return self.pk

    class Meta:
        db_table = "MTD_EFORM"
        managed = True


class EformFieldData(models.Model):
    eform_field_data_guid = models.CharField(db_column='EFORM_FIELD_DATA_GUID', primary_key=True, max_length=40, blank=False, null=False)
    cart_guid = models.CharField(db_column='CART_GUID', max_length=32, null=True)
    favourite_cart_guid = models.CharField(db_column='FAVOURITE_CART_GUID', max_length=32, null=True)
    eform_id = models.CharField(db_column='EFORM_ID', max_length=40, blank=False, null=True)
    eform_type = models.CharField(db_column='EFORM_TYPE', max_length=40, blank=False, null=False)
    eform_field_name = models.CharField(db_column='EFORM_FIELD_NAME', null=True, max_length=200)
    eform_field_data = models.CharField(db_column='EFORM_FIELD_DATA', null=True, max_length=1000)
    eform_field_count = models.PositiveIntegerField(db_column='EFORM_FIELD_COUNT', blank=False, null=True)
    eform_field_data_created_at = models.DateTimeField(db_column='EFORM_FIELD_DATA_CREATED_AT', blank=False, null=True)
    eform_field_data_created_by = models.CharField(db_column='EFORM_FIELD_DATA_CREATED_BY', max_length=12, blank=False, null=True)
    eform_field_data_changed_at = models.DateTimeField(db_column='EFORM_FIELD_DATA_CHANGED_AT', blank=True, null=True)
    eform_field_data_changed_by = models.CharField(db_column='EFORM_FIELD_DATA_CHANGED_BY', max_length=12, blank=False, null=True)
    eform_field_data_source_system = models.CharField(db_column='EFORM_FIELD_DATA_SOURCE_SYSTEM', max_length=20)
    eform_field_data_destination_system = models.CharField(db_column='EFORM_FIELD_DATA_DESTINATION_SYSTEM', max_length=20)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    item_guid = models.ForeignKey('eProc_Shopping_Cart.ScItem', models.DO_NOTHING, db_column='ITEM_GUID', null=True)
    po_item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='PO_ITEM_GUID',blank=True,null=True)
    product_eform_pricing_guid = models.ForeignKey('eProc_Configuration.ProductEformPricing', models.DO_NOTHING, db_column='product_eform_pricing_guid', null=True)

    class Meta:
        db_table = "MTD_EFORM_FIELD_DATA"
        managed = True