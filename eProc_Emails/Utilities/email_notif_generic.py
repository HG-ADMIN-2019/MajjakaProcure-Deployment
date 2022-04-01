"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    email_notif_generic.py
Usage:
   Generic functions to send email based on variant names.
   email_notify:function to send to email for user registration and returns the boolean value
   appr_notify:function to send email for approval registration and returns the boolean value
Author:
Soni Vydyula
"""
from django.core.mail import send_mail
import re
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import *
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Configuration.models import NotifSettings, NotifSettingsDesc
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.models import ScHeader, ScApproval

django_query_instance = DjangoQueries()


def email_notify(request, variant_name, client):
    """
    function to send an email for user registration
    :param client:
    :param request: request data from UI
    :param variant_name: takes the variant name for user registration
    :return: returns Boolean value
    """
    subject = ''
    body = ''
    # gets the email content based on the variant name
    emailDetail = django_query_instance.django_filter_only_query(NotifSettingsDesc, {
        'variant_name': variant_name, 'client': client
    }).values('notif_subject', 'notif_body')

    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['notif_subject']

    for bodyValue in emailDetail:
        body = bodyValue['notif_body']
    #  this function separates the keywords from the content.

    subjectKeys = re.findall('\&.*?\&', subject)
    bodyKeys = re.findall('\&.*?\&', body)
    keys = subjectKeys + bodyKeys

    # loop to assign the respective values based on the keywords from the email content
    for data in keys:
        if data == CONST_CLIENT:
            client = client
            subject = subject.replace(data, client)
            body = body.replace(data, client)
        if data == CONST_USER_NAME:
            username = request.POST['username']
            subject = subject.replace(data, username)
            body = body.replace(data, username)
        if data == CONST_PASSWORD:
            password = CONST_PWD
            body = body.replace(data, password)
        if data == CONST_FIRST_NAME:
            first_name = request.POST['first_name']
            subject = subject.replace(data, first_name)
            body = body.replace(data, first_name)
        if data == CONST_EMAIL:
            email = request.POST['email']
            subject = subject.replace(data, email)
            body = body.replace(data, email)
    # assigns to and from email
    to_mail = request.POST['email']
    From_Email = settings.EMAIL_HOST_USER
    To_Email = [to_mail]
    # main function to send an email.
    send_mail(subject, body, From_Email, To_Email, fail_silently=True)

    return True


# def send_mail():
#     # date = datetime.now()
#     # print(date)
#     tmp = UserData.objects.filter(client='700', username='soni').values('email')
#     subject = 'test mail'
#     body = 'test'
#     email = tmp['email']
#     From_Email = settings.EMAIL_HOST_USER
#     To_Email = [email]
#     send_mail(subject, body, From_Email, To_Email, fail_silently=True)
# schedule.every(5).minutes.do(send_mail)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)


def appr_notify():
    """
    :return: return the Boolean value
    """
    # gets the email content based on the variant name
    emailDetail = django_query_instance.django_filter_only_query(NotifSettings,
                                                                 {'variant_name': 'sc_approval'}).values('notif_subject'
                                                                                                         , 'notif_body')

    header_res = django_query_instance.django_filter_only_query(ScHeader,
                                                                {'doc_number': '9000008372'}).values('guid',
                                                                                                     'doc_number',
                                                                                                     'status',
                                                                                                     'requester',
                                                                                                     'created_at')
    for res in header_res:
        guid = res['guid']
        requester = res['requester']

    appr_res = django_query_instance.django_filter_only_query(ScApproval, {'header_guid': guid}).values('app_id')

    req_res = django_query_instance.django_filter_only_query(UserData,
                                                             {'username': requester}).values('first_name', 'email')

    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['notif_subject']

    for bodyValue in emailDetail:
        body = bodyValue['notif_body']
        #  this function separates the keywords from the content.
    subjectKeys = re.findall('\&.*?\&', subject)
    bodyKeys = re.findall('\&.*?\&', body)
    # loop to assign the respective values based on the keywords from the email content
    for data in subjectKeys and bodyKeys:
        if data == CONST_DOC_NUMBER:
            for keyWord in header_res:
                doc_number = keyWord['doc_number']
                subject = subject.replace(data, doc_number)
                body = body.replace(data, doc_number)
        if data == CONST_CREATED_AT:
            for keyWord in header_res:
                created_at = keyWord['created_at']
                created = str(created_at)
                subject = subject.replace(data, created)
                body = body.replace(data, created)
        if data == CONST_FIRST_NAME:
            for keyWord in req_res:
                first_name = keyWord['first_name']
                subject = subject.replace(data, first_name)
                body = body.replace(data, first_name)
        if data == CONST_APP_ID:
            for keyWord in appr_res:
                app_id = keyWord['app_id']
                subject = subject.replace(data, app_id)
                body = body.replace(data, app_id)

    From_Email = settings.EMAIL_HOST_USER
    for mails in req_res:
        to_email = mails['email']
    To_Email = [to_email]
    # main function to send an email.
    send_mail(subject, body, From_Email, To_Email, fail_silently=True)
    return True
