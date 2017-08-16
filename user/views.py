from rest_framework.authentication import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from .serializer import LoginSerializer


class Login(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    # {"phone":"12345678901","password":"abc12345"}
    def post(self, request):
        print(request.data)
        username = request.data.get('phone')
        password = request.data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                # login(request, user)
                # return redirect('/polls/')
                print('ok')
            return Response('okok', status=status.HTTP_200_OK)
        return Response('failed', status=status.HTTP_400_BAD_REQUEST)
