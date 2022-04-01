# Generated by Django 3.1.7 on 2021-12-27 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatContent',
            fields=[
                ('chat_content_guid', models.CharField(db_column='CHAT_CONTENT_GUID', max_length=32, primary_key=True, serialize=False)),
                ('room_no', models.CharField(db_column='ROOM_NO', max_length=60)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('chat_content', models.CharField(blank=True, db_column='CHAT_CONTENT', max_length=2000, null=True, verbose_name='Chat content')),
                ('chat_timestamp', models.DateTimeField(auto_now_add=True, db_column='CHAT_TIMESTAMP')),
                ('Chat_content_created_at', models.DateTimeField(blank=True, db_column='CHAT_CONTENT_CREATED_AT', null=True)),
                ('Chat_content_created_by', models.CharField(db_column='CHAT_CONTENT_CREATED_BY', max_length=30, null=True)),
                ('Chat_content_changed_at', models.DateTimeField(blank=True, db_column='CHAT_CONTENT_CHANGED_AT', null=True)),
                ('Chat_content_changed_by', models.CharField(db_column='CHAT_CONTENT_CHANGED_BY', max_length=30, null=True)),
                ('del_ind', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'MTD_CHAT_CONTENT',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ChatParticipants',
            fields=[
                ('chat_participants_guid', models.CharField(db_column='CHAT_PARTICIPANTS_GUID', max_length=32, primary_key=True, serialize=False)),
                ('room_no', models.CharField(db_column='ROOM_NO', max_length=60)),
                ('room_name', models.CharField(blank=True, db_column='room_name', max_length=300, null=True)),
                ('username', models.CharField(db_column='USERNAME', max_length=16)),
                ('chat_type', models.CharField(db_column='CHAT_TYPE', max_length=30)),
                ('Chat_created_at', models.DateTimeField(blank=True, db_column='CHAT_CREATED_AT', null=True, verbose_name='Created At')),
                ('Chat_created_by', models.CharField(db_column='CHAT_CREATED_BY', max_length=30, null=True, verbose_name='Created by')),
                ('Chat_changed_at', models.DateTimeField(blank=True, db_column='CHAT_CHANGED_AT', null=True, verbose_name='Changed At')),
                ('Chat_changed_by', models.CharField(db_column='CHAT_CHANGED_BY', max_length=30, null=True, verbose_name='Changed By')),
                ('del_ind', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'MTD_CHAT_PARTICIPANTS',
                'managed': True,
            },
        ),
    ]
