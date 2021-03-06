# Generated by Django 3.1.7 on 2022-05-31 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Purchase_Order', '0003_auto_20220531_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poitem',
            name='prod_type',
            field=models.CharField(blank=True, db_column='PROD_TYPE', max_length=2, verbose_name='Product Type'),
        ),
        migrations.AlterField(
            model_name='poitem',
            name='rfq_item_num',
            field=models.PositiveIntegerField(blank=True, db_column='RFQ_ITEM_NUM', null=True, verbose_name='Line Number'),
        ),
    ]
