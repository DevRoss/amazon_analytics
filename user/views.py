from rest_framework.authentication import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib.auth import logout, login
from rest_framework.authentication import SessionAuthentication

"""
默认验证方式是session
default: settings.REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES
"""


class Login(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    # {"phone":"12345678901","password":"abc12345"}
    def post(self, request):
        username = request.data.get('phone')
        password = request.data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                ret_json = {
                    "error_code": 0,
                    "detail": "login successfully"
                }
                return Response(ret_json, status=status.HTTP_200_OK)
        return Response('failed', status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        logout(request)
        ret_json = {
            "error_code": 0,
            "detail": "logout successfully"
        }
        return Response(ret_json, status=status.HTTP_200_OK)