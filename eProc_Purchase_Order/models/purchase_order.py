import operator
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from eProc_Shopping_Cart.models import DBQueries


class PoHeader(models.Model, DBQueries):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    doc_number = models.CharField(db_column='DOC_NUMBER', max_length=10, blank=False, null=False, verbose_name='PO Number')
    version_type = models.CharField(db_column='VERSION_TYPE', max_length=1, blank=True, null=False, verbose_name='Version type')
    version_num = models.CharField(db_column='VERSION_NUM', max_length=8, blank=True, null=False, verbose_name='Version number')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=False, verbose_name='PO NAME')
    total_value = models.CharField(db_column='TOTAL_VALUE', max_length=20, blank=False, null=False, verbose_name='Total Value')
    currency = models.CharField(db_column='CURRENCY', max_length=5, blank=False, null=False, verbose_name='Currency')
    requester = models.CharField(db_column='REQUESTER', max_length=12, blank=False, null=False, verbose_name='Requester')
    status = models.CharField(db_column='STATUS', max_length=20, blank=False, null=False, verbose_name='Status')
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, verbose_name='Created At')
    created_by = models.CharField(db_column='CREATED_BY', max_length=12, blank=False, null=False, verbose_name='Creator')
    changed_at = models.DateTimeField(db_column='CHANGED_AT', blank=True, null=False, verbose_name='Changed At')
    changed_by = models.CharField(db_column='CHANGED_BY', max_length=12, blank=False, null=False, verbose_name='Changed By')
    ordered_at = models.DateTimeField(db_column='ORDERED_AT',blank=True, null=True, verbose_name='Ordered At')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=False, verbose_name='Time Zone')
    item_cat = models.CharField(db_column='ITEM_CAT', max_length=4, blank=False, null=True, verbose_name='Item Category')
    limit = models.CharField(db_column='LIMIT', max_length=20, blank=True, null=True, verbose_name='Limit')
    expected_value = models.DecimalField(db_column='EXPECTED_VALUE', max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='expected value')
    unlimited = models.CharField(db_column='UNLIMITED', max_length=1, blank=True, null=True, verbose_name='Unlimited')
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=12, blank=True, null=True, verbose_name='Supplier ID')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        managed = True
        unique_together = ('client', 'doc_number')
        db_table = 'MTD_PO_HEADER'

# Get header data by supplier id
    def get_hdr_data_by_supplier(self, sup_id):
        return PoHeader.objects.filter(supplier_id=sup_id).distinct()

# Get header data by guid
    def get_hdr_data_by_guid(self, guid):
        return PoHeader.objects.filter(guid=guid)

# Get header guid by object id
    @staticmethod
    def get_hdr_guid_by_objid(objid):
        try:
            hdr = PoHeader.objects.get(doc_number=objid)
            return getattr(hdr, 'guid')
        except ObjectDoesNotExist:
            return 'error'
        except MultipleObjectsReturned:
            hdr = PoHeader.objects.filter(doc_number=objid)
            hdr = sorted(hdr, key=operator.attrgetter('version_num'))
            return getattr(hdr[0], 'guid')

# Get object id by guid
    @staticmethod
    def get_objid_by_guid(guid):
        try:
            return str(getattr(PoHeader.objects.get(guid=guid), 'doc_number'))
        except:
            return ''

class PoItem(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    po_item_num = models.CharField(db_column='PO_ITEM_NUM',max_length=10, blank=True, null=True, verbose_name='Line Number')
    sc_num = models.CharField(db_column='SC_NUM', max_length=10, blank=True, null=True, verbose_name='SC Number')
    sc_header_guid = models.CharField(db_column='SC_HEADER_GUID', max_length=32, blank=True, null=True)
    item_num = models.DecimalField(db_column='ITEM_NUM', max_digits=10, decimal_places=0, blank=True, null=True,verbose_name='Item Number')
    sc_item_guid = models.CharField(db_column='SC_ITEM_GUID', max_length=32, blank=True, null=True)
    prod_description = models.CharField(db_column='PROD_DESCRIPTION', max_length=255, blank=False, null=False, verbose_name='Description')
    comp_code = models.CharField(db_column='COMP_CODE', max_length=10, blank=False, null=False, verbose_name='Company Code')
    purch_grp = models.CharField(db_column='PURCH_GRP', max_length=20, blank=True, null=True, verbose_name='Purchasing Group')
    purch_org = models.CharField(db_column='PURCH_ORG', max_length=20, blank=True, null=True, verbose_name='Purchasing Organization')
    item_del_date = models.DateField(db_column='ITEM_DEL_DATE', max_length=10, blank=False, null=True, verbose_name='Delivery Date')
    prod_cat = models.CharField(db_column='PROD_CAT', max_length=20, blank=False, null=False, verbose_name='Product Category')
    hiring_level = models.CharField(db_column='HIRING_LEVEL', max_length=64, blank=True, null=True)
    hiring_role = models.CharField(db_column='HIRING_ROLE', max_length=64, blank=True, null=True)
    hiring_skill = models.CharField(db_column='HIRING_SKILL', max_length=64, blank=True, null=True)
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=2, blank=False, null=False, verbose_name='Product Type')
    catalog_id = models.CharField(db_column='CATALOG_ID', max_length=20, blank=True, null=True, verbose_name='Catalog ID')
    unspsc = models.CharField(db_column='UNSPSC', max_length=10, blank=True, null=True, verbose_name='UNSPSC')
    fin_entry_ind = models.CharField(db_column='FIN_ENTRY_IND',max_length=1, blank=True, null=True, verbose_name='Fin entry ind')
    quantity = models.CharField(db_column='QUANTITY', max_length=20, blank=True, null=True, verbose_name='Quantity')
    price = models.DecimalField(db_column='PRICE', max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Price')
    price_unit = models.CharField(db_column='PRICE_UNIT', max_length=5, blank=True, null=True, verbose_name='Price Unit')
    unit = models.CharField(db_column='UNIT', max_length=3, blank=False, null=False, verbose_name='Unit')
    gross_price = models.DecimalField(db_column='GROSS_PRICE', max_digits=15, decimal_places=2, blank=False, null=False, verbose_name='Gross Price')
    gr_ind = models.CharField(db_column='GR_IND', max_length=1, blank=True, null=True, verbose_name='Gr ind')
    supp_prod_num = models.CharField(db_column='SUPP_PROD_NUM', max_length=40, blank=True, null=True, verbose_name='Supplier Product Number')
    manu_part_num = models.CharField(db_column='MANU_PART_NUM', max_length=40, blank=True, null=True, verbose_name='manu part num')
    manu_code_num = models.CharField(db_column='MANU_CODE_NUM', max_length=10, blank=True, null=True, verbose_name='manu code num')
    ctr_num = models.CharField(db_column='CTR_NUM', max_length=50, blank=True, null=True, verbose_name='ctr num')
    supp_ord_addr = models.CharField(db_column='SUPP_ORD_ADDR', max_length=10, blank=True, null=True, verbose_name='Supplier Ordering Address')
    del_srm_purch_doc = models.CharField(db_column='DEL_SRM_PURCH_DOC', max_length=12, blank=True, null=True,verbose_name='Deletion Indicator SRM Purchasing Document')
    bill_to_addr_num = models.CharField(db_column='BILL_TO_ADDR_NUM', max_length=10, blank=False, null=False, verbose_name='bill to addr num')
    ship_to_addr_num = models.CharField(db_column='SHIP_TO_ADDR_NUM', max_length=10, blank=False, null=False, verbose_name='ship to addr num')
    goods_recep = models.CharField(db_column='GOODS_RECEP', max_length=12, blank=False, null=False,verbose_name='Goods Recipient')
    manu_name = models.CharField(db_column='MANU_NAME', max_length=50, blank=True, null=True, verbose_name='manu name')
    del_time_days = models.CharField(db_column='DEL_TIME_DAYS', max_length=5, blank=True, null=True, verbose_name='Delivery Days')
    internal_note = models.CharField(db_column='INTERNAL_NOTE', max_length=1000, blank=True, null=True, verbose_name='Internal Note')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    header_guid = models.ForeignKey('eProc_Purchase_Order.PoHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=False, null=False)

    class Meta:
        managed  = True
        db_table = 'MTD_PO_ITEM'

# Get item data by header guid
    def get_itms_by_guid(self, hdr_guid):
        return PoItem.objects.filter(header_guid=hdr_guid).order_by('po_item_num')

class PoApproval(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    step_num = models.CharField(db_column='STEP_NUM', max_length=3, blank=True, null=True, verbose_name='Sequence')
    app_desc = models.CharField(db_column='APP_DESC', max_length=60, blank=True, null=True, verbose_name='Agent Determination')
    proc_lvl_sts = models.CharField(db_column='PROC_LVL_STS', max_length=10, blank=True, null=True, verbose_name='Level Status')
    app_sts = models.CharField(db_column='APP_STS', max_length=20, blank=True, null=True, verbose_name='Status')
    app_id = models.CharField(db_column='APP_ID', max_length=70, blank=True, null=True, verbose_name='Processor')
    received_time = models.DateTimeField(db_column='received_time', max_length=32, blank=True, null=True, verbose_name='Received On')
    proc_time = models.DateTimeField(db_column='PROC_TIME', max_length=32, blank=True, null=True, verbose_name='Processed On')
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6, blank=True, null=True, verbose_name='Time Zone')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    header_guid = models.ForeignKey('PoHeader', models.DO_NOTHING, db_column='HEADER_GUID', blank=True, null=True)

    class Meta:
        managed  = True
        db_table = 'MTD_PO_APPROVAL'

# Get approval data by header guid
    def get_apprs_by_guid(self, hdr_guid):
        app_data = PoApproval.objects.filter(header_guid=hdr_guid).order_by('step_num')
        return app_data


class PoAccounting(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    acc_item_num = models.DecimalField(db_column='ACC_ITEM_NUM', max_digits=4, decimal_places=0, blank=False, null=False, verbose_name='Number')
    acc_cat = models.CharField(db_column='ACC_CAT', max_length=5, blank=False, null=False, verbose_name='Account Assignment Category')
    dist_perc = models.CharField(db_column='DIST_PERC', max_length=6, blank=True, null=True, verbose_name='Distribution Percentage')
    gl_acc_num = models.CharField(db_column='GL_ACC_NUM', max_length=10, blank=False, null=False, verbose_name='General Ledger Account')
    cost_center = models.CharField(db_column='COST_CENTER', max_length=10, blank=True, null=True, verbose_name='Cost Center')
    internal_order = models.CharField(db_column='INTERNAL_ORDER', max_length=12, blank=True, null=True, verbose_name='Internal Order')
    generic_acc_ass = models.CharField(db_column='GENERIC_ACC_ASS', max_length=64, blank=True, null=True, verbose_name='Generic Acc Ass')
    wbs_ele = models.CharField(db_column='WBS_ELE', max_length=24, blank=True, null=True, verbose_name='WBS Element')
    project = models.CharField(db_column='PROJECT', max_length=24, blank=True, null=True, verbose_name='Project')
    task_id = models.CharField(db_column='TASK_ID', max_length=25, blank=True, null=True, verbose_name='Task Id')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    item_guid = models.ForeignKey('eProc_Purchase_Order.PoItem', models.DO_NOTHING, db_column='ITEM_GUID', blank=True, null=True)

    class Meta:
        managed  = True
        db_table = 'MTD_PO_ACCOUNTING'

# Get accounting data by item guid
    def get_acc_data_by_guid(self, itm_guid):
        return PoAccounting.objects.filter(item_guid__in=itm_guid).order_by('acc_item_num')
