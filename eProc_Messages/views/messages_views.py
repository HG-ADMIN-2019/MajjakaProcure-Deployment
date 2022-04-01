from datetime import datetime, date

from django.shortcuts import render
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import get_country_id, getClients
from eProc_Basic.Utilities.functions.messages_config import get_message_description
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data
from eProc_Configuration.models import SupplierMaster, Languages
from eProc_Suppliers.Utilities.supplier_generic import supplier_detail_search
from eProc_Configuration.models.development_data import MessagesId, MessagesIdDesc, FieldTypeDesc

django_query_instance = DjangoQueries()



