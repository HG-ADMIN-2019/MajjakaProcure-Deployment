# Generated by Django 3.1.7 on 2022-06-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Emails', '0004_auto_20220610_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildocumentmonitoring',
            name='error_type',
            field=models.CharField(db_column='ERROR_TYPE', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailusermonitoring',
            name='error_type',
            field=models.CharField(db_column='ERROR_TYPE', max_length=20, null=True),
        ),
    ]
