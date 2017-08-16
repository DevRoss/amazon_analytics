# coding: utf-8
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser
from .serializer import AddTopSellerSerializer
from .models import TopSeller, Keyword
import datetime


# /api/v1/topseller?category=<category>&strat_time=<20170101>&end_time=<20170201>
class AddTopSeller(CreateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = AddTopSellerSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddTopSellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = serializer.validated_data.get('category')
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')

            try:
                obj = TopSeller.objects.get(user=request.user, title=category)
            except TopSeller.DoesNotExist:
                # 关键词不存在

                print('does not exist')
                ret_json = {
                    "error_code": 0,
                    "detail": category + " is created",
                    "start_time": start_time,
                    "end_time": end_time,
                }
                return Response(ret_json, status=status.HTTP_201_CREATED, headers=self.headers)
            return Response('This category already exists', status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
