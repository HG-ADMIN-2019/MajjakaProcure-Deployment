import datetime
from eProc_Basic.Utilities.constants.constants import CONST_SUPPLIER_IMAGE_TYPE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import guid_generator
from eProc_Basic.Utilities.functions.image_type_funtions import get_image_type
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Configuration.models import OrgClients, ImagesUpload

django_query_instance = DjangoQueries()


def save_supplier_image(supplier_file, supplier_id, supplier_image_name):
    image_type = get_image_type(CONST_SUPPLIER_IMAGE_TYPE)
    client = global_variables.GLOBAL_CLIENT
    if image_type:
        if django_query_instance.django_existence_check(ImagesUpload, {
            'image_id': supplier_id,
            'client': client,
            'image_type': image_type
        }):

            supplier_image_guid = django_query_instance.django_filter_value_list_query(ImagesUpload, {
                'image_id': supplier_id, 'client': client, 'image_type': image_type
            }, 'images_upload_guid')

            for image_guid in supplier_image_guid:
                django_query_instance.django_get_query(ImagesUpload, {'images_upload_guid': image_guid}).image_url.delete(save=True)
                django_query_instance.django_get_query(ImagesUpload, {'images_upload_guid': image_guid}).delete()

    django_query_instance.django_create_query(ImagesUpload, {
        'images_upload_guid': guid_generator(),
        'client': django_query_instance.django_get_query(OrgClients, {'client': client}),
        'image_id': supplier_id,
        'image_url': supplier_file,
        'image_name': supplier_image_name,
        'image_default': True,
        'image_type': CONST_SUPPLIER_IMAGE_TYPE,
        'created_at': datetime.date.today(),
        'created_by': global_variables.GLOBAL_LOGIN_USERNAME
    })
