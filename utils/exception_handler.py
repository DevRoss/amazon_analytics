from rest_framework.views import exception_handler
from rest_framework import exceptions
from django.http.response import Http404
from django.core.exceptions import PermissionDenied
from . import extra_exceptions

"""
+-----------------------+----------------+
|       exception       |   error_code   |
+=======================|================+
|     APIException      |        1       |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+
|                       |               |
+-----------------------+----------------+

"""


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # 扩展原来的exception, 添加error_code

    if isinstance(exc, Http404):
        response.data['error_code'] = 2

    elif isinstance(exc, exceptions.NotFound):
        response.data['error_code'] = 2

    elif isinstance(exc, exceptions.MethodNotAllowed):
        response.data['error_code'] = 3

    elif isinstance(exc, exceptions.NotAcceptable):
        response.data['error_code'] = 4

    elif isinstance(exc, exceptions.Throttled):
        response.data['error_code'] = 5

    elif isinstance(exc, exceptions.ParseError):
        response.data['error_code'] = 10

    elif isinstance(exc, exceptions.ValidationError):
        response.data['error_code'] = 11

    elif isinstance(exc, exceptions.UnsupportedMediaType):
        response.data['error_code'] = 12

    elif isinstance(exc, extra_exceptions.ItemExists):
        response.data['error_code'] = 13

    elif isinstance(exc, extra_exceptions.ItemDoesNotExist):
        response.data['error_code'] = 14

    elif isinstance(exc, PermissionDenied):
        response.data['error_code'] = 20

    elif isinstance(exc, exceptions.AuthenticationFailed):
        response.data['error_code'] = 21

    elif isinstance(exc, exceptions.NotAuthenticated):
        response.data['error_code'] = 22

    return response
