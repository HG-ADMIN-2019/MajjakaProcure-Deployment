# Generated by Django 3.1.7 on 2022-06-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Configuration', '0002_auto_20220519_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcontents',
            name='footer',
            field=models.TextField(blank=True, db_column='FOOTER', null=True),
        ),
        migrations.AddField(
            model_name='emailcontents',
            name='header',
            field=models.TextField(blank=True, db_column='HEADER', null=True),
        ),
    ]
