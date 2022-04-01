# Generated by Django 3.1.7 on 2021-12-27 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentlyViewedProducts',
            fields=[
                ('recently_viewed_prod_guid', models.CharField(db_column='RECENTLY_VIEWED_PROD_GUID', default=None, max_length=32, primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('product_id', models.CharField(db_column='PRODUCT_ID', max_length=16, null=True)),
                ('catalog_id', models.CharField(db_column='CATALOG_ID', default=None, max_length=16)),
                ('recently_viewed_prod_created_at', models.DateTimeField(blank=True, db_column='RECENTLY_VIEWED_PROD_CREATED_AT', null=True)),
                ('recently_viewed_prod_created_by', models.CharField(db_column='RECENTLY_VIEWED_PROD_CREATED_BY', max_length=30, null=True)),
                ('recently_viewed_prod_changed_at', models.DateTimeField(blank=True, db_column='RECENTLY_VIEWED_PROD_CHANGED_AT', null=True)),
                ('recently_viewed_prod_changed_by', models.CharField(db_column='RECENTLY_VIEWED_PROD_CHANGED_BY', max_length=30, null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
            ],
            options={
                'db_table': 'MTD_RECENTLY_VIEWED_PRODUCTS',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FavouriteCart',
            fields=[
                ('favourite_cart_guid', models.CharField(db_column='FAVOURITE_CART_GUID', default=None, max_length=32, primary_key=True, serialize=False)),
                ('favourite_cart_number', models.PositiveIntegerField(db_column='FAVOURITE_CART_NUMBER', verbose_name='Favourite Cart Number')),
                ('favourite_cart_name', models.CharField(blank=True, db_column='FAVOURITE_CART_NAME', max_length=255, null=True, verbose_name='Favourite cart Name')),
                ('item_num', models.PositiveIntegerField(db_column='ITEM_NUM', null=True, verbose_name='Item Number')),
                ('description', models.CharField(db_column='DESCRIPTION', max_length=250, null=True)),
                ('prod_cat_desc', models.CharField(db_column='PROD_CAT_DESC', max_length=255, null=True, verbose_name='Product Category Description')),
                ('prod_cat', models.CharField(db_column='PROD_CAT', max_length=20, null=True)),
                ('int_product_id', models.CharField(db_column='INT_PRODUCT_ID', max_length=20, null=True)),
                ('ext_product_id', models.PositiveIntegerField(blank=True, db_column='EXT_PRODUCT_ID', null=True)),
                ('quantity', models.CharField(db_column='QUANTITY', max_length=20, null=True)),
                ('unit', models.CharField(db_column='UNIT', max_length=30, null=True)),
                ('price', models.DecimalField(db_column='PRICE', decimal_places=2, max_digits=15, null=True)),
                ('gross_price', models.DecimalField(db_column='GROSS_PRICE', decimal_places=2, max_digits=13, null=True)),
                ('price_unit', models.CharField(db_column='PRICE_UNIT', max_length=5, null=True)),
                ('currency', models.CharField(db_column='CURRENCY', max_length=3, null=True)),
                ('supplier_id', models.CharField(db_column='SUPPLIER_ID', max_length=10, null=True)),
                ('pref_supplier', models.CharField(db_column='PREF_SUPPLIER', max_length=10, null=True)),
                ('lead_time', models.PositiveIntegerField(db_column='LEAD_TIME', null=True)),
                ('value', models.CharField(db_column='VALUE', max_length=20, null=True)),
                ('fc_total_value', models.CharField(db_column='FC_TOTAL_VALUE', max_length=15, null=True, verbose_name='Total Value')),
                ('fc_total_currency', models.CharField(db_column='FC_TOTAL_CURRENCY', max_length=3, null=True, verbose_name='Currency')),
                ('supp_txt', models.CharField(blank=True, db_column='SUPP_TXT', max_length=1000, null=True, verbose_name='Supplier Text')),
                ('manu_part_num', models.CharField(db_column='MANU_PART_NUM', max_length=40, null=True)),
                ('manu_code_num', models.CharField(db_column='MANU_CODE_NUM', max_length=10, null=True)),
                ('supp_prod_num', models.CharField(db_column='SUPP_PROD_NUM', max_length=40, null=True)),
                ('call_off', models.CharField(db_column='CALL_OFF', max_length=15, null=True)),
                ('supplier_contact', models.CharField(blank=True, db_column='SUPPLIER_CONTACT', max_length=40, null=True)),
                ('supplier_fax_no', models.CharField(blank=True, db_column='SUPPLIER_FAX_NO', max_length=30, null=True)),
                ('supplier_email', models.CharField(blank=True, db_column='SUPPLIER_EMAIL', max_length=100, null=True)),
                ('quantity_min', models.PositiveIntegerField(db_column='QUANTITY_MIN', null=True)),
                ('value_min', models.PositiveIntegerField(db_column='VALUE_MIN', null=True)),
                ('tiered_flag', models.BooleanField(db_column='TIERED_FLAG', null=True)),
                ('bundle_flag', models.BooleanField(db_column='BUNDLE_FLAG', null=True)),
                ('tax_code', models.CharField(db_column='TAX_CODE', max_length=5, null=True, verbose_name='Tax Code')),
                ('delivery_days', models.DateField(db_column='DELIVERY_DAYS', null=True)),
                ('catalog_id', models.CharField(db_column='CATALOG_ID', max_length=20, null=True)),
                ('catalog_item', models.CharField(db_column='CATALOG_ITEM', max_length=32, null=True)),
                ('ctr_num', models.CharField(db_column='CTR_NUM', max_length=50, null=True)),
                ('contract', models.CharField(db_column='contract', max_length=50, null=True)),
                ('prod_type', models.CharField(db_column='PROD_TYPE', max_length=2, null=True)),
                ('item_del_date', models.DateField(db_column='ITEM_DEL_DATE', null=True)),
                ('process_type', models.CharField(db_column='PROCESS_TYPE', max_length=8, null=True)),
                ('start_date', models.DateField(db_column='START_DATE', null=True)),
                ('end_date', models.DateField(db_column='END_DATE', null=True)),
                ('ir_gr_ind', models.BooleanField(db_column='IR_GR_IND', null=True)),
                ('gr_ind', models.BooleanField(db_column='GR_IND', null=True, verbose_name='Gr ind')),
                ('overall_limit', models.DecimalField(db_column='OVERALL_LIMIT', decimal_places=2, max_digits=15, null=True)),
                ('expected_value', models.DecimalField(db_column='EXPECTED_VALUE', decimal_places=2, max_digits=15, null=True)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('eform_id', models.CharField(db_column='EFORM_ID', max_length=40, null=True)),
                ('favourite_cart_created_at', models.DateTimeField(blank=True, db_column='FAVOURITE_CART_CREATED_AT', null=True)),
                ('favourite_cart_created_by', models.CharField(db_column='FAVOURITE_CART_CREATED_BY', max_length=30, null=True)),
                ('favourite_cart_changed_at', models.DateTimeField(blank=True, db_column='FAVOURITE_CART_CHANGED_AT', null=True)),
                ('favourite_cart_changed_by', models.CharField(db_column='FAVOURITE_CART_CHANGED_BY', max_length=30, null=True)),
                ('favourite_cart_source_system', models.CharField(db_column='FAVOURITE_CART_SOURCE_SYSTEM', max_length=20)),
                ('favourite_cart_destination_system', models.CharField(db_column='FAVOURITE_CART_DESTINATION_SYSTEM', max_length=20)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
            ],
            options={
                'db_table': 'MTD_FAVOURITE_CART',
                'managed': True,
            },
        ),
    ]
