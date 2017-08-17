# coding: utf-8
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser
from .serializer import AddTopSellerSerializer, AddKeywordSerializer, TimeTopSerializer
from .models import TopSeller, Keyword
import datetime
from amazon_analytics.settings import KEYWORD_FILE_URL, TOPSELLER_FILE_URL


# /api/v1/topseller?category=<category>&strat_time=<20170101>&end_time=<20170201>
class AddTopSeller(CreateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = AddTopSellerSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddTopSellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            category = serializer.validated_data.get('category')
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')

            try:
                obj = TopSeller.objects.get(user=user, title=category)
            except TopSeller.DoesNotExist:
                # 关键词不存在
                obj = TopSeller(user=user, title=category,
                                result_file=os.path.join(TOPSELLER_FILE_URL, user.phone, category))
                obj.save()
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


class AddKeyword(CreateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = AddKeywordSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddKeywordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            keyword = serializer.validated_data.get('keyword')

            try:
                obj = keyword.objects.get(user=user, title=keyword)
            except Keyword.DoesNotExist:
                # 关键词不存在
                print('does not exist')

                obj = Keyword(user=user, title=keyword, result_file=os.path.join(KEYWORD_FILE_URL, user, keyword))
                obj.save()
                ret_json = {
                    "error_code": 0,
                    "detail": keyword + " is created",
                }
                return Response(ret_json, status=status.HTTP_201_CREATED, headers=self.headers)
            return Response('This category already exists', status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetTimeTop(APIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        try:
            obj = TopSeller.objects.get(user=request.user, title=category)
        except TopSeller.DoesNotExist:
            # 用户没有添加任务，返回403
            return Response(status=status.HTTP_403_FORBIDDEN)
        # print(self.queryset.count())
        serializer = TimeTopSerializer(data=request.GET.dict())
        if serializer.is_valid(raise_exception=True):

            # do something
            print(obj.result_file)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)
