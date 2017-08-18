from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import ugettext_lazy as _


class ItemExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Item is already exists.')
    default_code = 'invalid'
