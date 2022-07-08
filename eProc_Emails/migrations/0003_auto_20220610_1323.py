# Generated by Django 3.1.7 on 2022-06-10 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Configuration', '0004_messagesiddesc_messages_category'),
        ('eProc_Emails', '0002_auto_20220609_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildocumentmonitoring',
            name='email_contents_guid',
            field=models.ForeignKey(db_column='EMAIL_CONTENTS_GUID', on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.emailcontents'),
        ),
    ]
