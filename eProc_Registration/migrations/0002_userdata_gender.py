# Generated by Django 3.1.7 on 2022-06-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProc_Registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='gender',
            field=models.CharField(blank=True, db_column='GENDER', max_length=12, null=True),
        ),
    ]
