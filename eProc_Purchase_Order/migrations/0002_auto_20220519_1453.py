# Generated by Django 3.1.7 on 2022-05-19 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Shopping_Cart', '0001_initial'),
        ('eProc_Configuration', '0002_auto_20220519_1453'),
        ('eProc_Purchase_Order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poitem',
            name='sc_header_guid',
            field=models.ForeignKey(blank=True, db_column='SC_HEADER_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Shopping_Cart.scheader'),
        ),
        migrations.AddField(
            model_name='poitem',
            name='sc_item_guid',
            field=models.ForeignKey(blank=True, db_column='SC_ITEM_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Shopping_Cart.scitem'),
        ),
        migrations.AddField(
            model_name='poheader',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients'),
        ),
        migrations.AddField(
            model_name='poapproval',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients'),
        ),
        migrations.AddField(
            model_name='poapproval',
            name='po_header_guid',
            field=models.ForeignKey(db_column='PO_HEADER_GUID', on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poheader'),
        ),
        migrations.AddField(
            model_name='poapproval',
            name='po_item_guid',
            field=models.ForeignKey(blank=True, db_column='PO_ITEM_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poitem'),
        ),
        migrations.AddField(
            model_name='poaddresses',
            name='address_partner_type',
            field=models.ForeignKey(db_column='ADDRESS_PARTNER_TYPE', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Configuration.addresspartnertype'),
        ),
        migrations.AddField(
            model_name='poaddresses',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients'),
        ),
        migrations.AddField(
            model_name='poaddresses',
            name='po_header_guid',
            field=models.ForeignKey(db_column='PO_HEADER_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poheader'),
        ),
        migrations.AddField(
            model_name='poaddresses',
            name='po_item_guid',
            field=models.ForeignKey(blank=True, db_column='PO_ITEM_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poitem'),
        ),
        migrations.AddField(
            model_name='poaccounting',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients'),
        ),
        migrations.AddField(
            model_name='poaccounting',
            name='po_header_guid',
            field=models.ForeignKey(blank=True, db_column='PO_HEADER_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poheader'),
        ),
        migrations.AddField(
            model_name='poaccounting',
            name='po_item_guid',
            field=models.ForeignKey(blank=True, db_column='PO_ITEM_GUID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eProc_Purchase_Order.poitem'),
        ),
        migrations.AlterUniqueTogether(
            name='poheader',
            unique_together={('client', 'doc_number')},
        ),
    ]
