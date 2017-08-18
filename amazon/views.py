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
from rest_framework import exceptions
from utils import extra_exceptions


class ModelObject:
    def __init__(self):
        self.instance = None

    def has_data(self, model, **kwargs):
        """

        :param model: 要查询的对象
        :param kwargs: 过滤器字段
        :return: True (会修改instance为model对象)/False
        """
        try:
            self.instance = model.objects.get(**kwargs)
            return True
        except model.DoesNotExist:
            # 关键词不存在
            return False


# /api/v1/topseller?category=<category>&strat_time=<20170101>&end_time=<20170201>
class AddTopSeller(CreateAPIView):
    serializer_class = AddTopSellerSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddTopSellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            category = serializer.validated_data.get('category')
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')
            obj = ModelObject()
            if obj.has_data(TopSeller, user=user, title=category):
                raise extra_exceptions.ItemExists('This TopSeller is already exists.')
            else:
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


class AddKeyword(CreateAPIView):
    serializer_class = AddKeywordSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddKeywordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            keyword = serializer.validated_data.get('keyword')
            obj = ModelObject()
            if obj.has_data(Keyword, user=user, title=keyword):
                raise extra_exceptions.ItemExists('This Keyword is already exists.')
            else:
                # 关键词不存在
                print('does not exist')

                obj = Keyword(user=user, title=keyword, result_file=os.path.join(KEYWORD_FILE_URL, user.phone, keyword))
                obj.save()
                ret_json = {
                    "error_code": 0,
                    "detail": keyword + " is created",
                }
                return Response(ret_json, status=status.HTTP_201_CREATED, headers=self.headers)


class GetTimeTop(ListAPIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        user = request.user
        try:
            obj = TopSeller.objects.get(user=user, title=category)
        except TopSeller.DoesNotExist:
            # 用户没有添加任务，返回403
            raise extra_exceptions.ItemDoesNotExist('This category does not exist.')
        serializer = TimeTopSerializer(data=request.GET.dict())
        if serializer.is_valid(raise_exception=True):
            # do something
            print(obj.result_file)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetAmazonList(ListAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')

        obj = ModelObject()
        if category:
            if obj.has_data(TopSeller, user=user, title=category):
                result_file = obj.instance.result_file
                print(result_file)
                return Response(result_file, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        elif keyword:
            if obj.has_data(Keyword, user=user, title=keyword):
                result_file = obj.instance.result_file
                print(result_file)
                return Response(result_file, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
