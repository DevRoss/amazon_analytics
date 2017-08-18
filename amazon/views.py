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


class AddTopSeller(CreateAPIView):
    serializer_class = AddTopSellerSerializer

    def post(self, request, *args, **kwargs):
        """

            http://127.0.0.1:8000/api/v1/add-topseller
        """
        serializer = AddTopSellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user  # 获取登录用户
            category = serializer.validated_data.get('category')  # 在post表单中的到category
            start_time = serializer.validated_data.get('start_time')  # 在post表单中的到start_time, 没有的话返回None
            end_time = serializer.validated_data.get('end_time')  # 在post表单中的到end_time, 没有的话返回None
            obj = ModelObject()
            if obj.has_data(TopSeller, user=user, title=category):
                # 关键词存在
                raise extra_exceptions.ItemExists('This TopSeller is already exists.')
            else:
                # 关键词不存在
                obj = TopSeller(user=user, title=category,
                                result_file=os.path.join(TOPSELLER_FILE_URL, user.phone, category))
                obj.save()
                # print('does not exist')
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
        """

            http://127.0.0.1:8000/api/v1/add-keyword
        """
        user = request.user  # 获取登录用户
        serializer = AddKeywordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            keyword = serializer.validated_data.get('keyword')
            obj = ModelObject()
            if obj.has_data(Keyword, user=user, title=keyword):
                # 关键词存在
                raise extra_exceptions.ItemExists('This Keyword is already exists.')
            else:
                # 关键词不存在
                # print('does not exist')

                obj = Keyword(user=user, title=keyword, result_file=os.path.join(KEYWORD_FILE_URL, user.phone, keyword))
                obj.save()
                ret_json = {
                    "error_code": 0,
                    "detail": keyword + " is created",
                }
                return Response(ret_json, status=status.HTTP_201_CREATED, headers=self.headers)


class GetTimeTop(ListAPIView):
    def get(self, request, *args, **kwargs):
        """

        http://127.0.0.1:8000/api/v1/get-topseller?category=123412342134123&start_time=2017-1-2
        end_time 默认为今天
        start_time 默认为 end_time - 30天
        """
        category = request.GET.get('category')  # 在url中获取 category
        user = request.user  # 获取登录用户
        try:
            obj = TopSeller.objects.get(user=user, title=category)
        except TopSeller.DoesNotExist:
            raise extra_exceptions.ItemDoesNotExist('This category does not exist.')
        serializer = TimeTopSerializer(data=request.GET.dict())
        if serializer.is_valid(raise_exception=True):
            # do something
            print(obj.result_file)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetAmazonList(ListAPIView):
    def get(self, request, *args, **kwargs):
        """
        http://127.0.0.1:8000/api/v1/get-amazonlist?category=123123&keyword=123123
        """
        user = request.user
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')
        result_file_list = list()
        obj = ModelObject()
        if category:
            if obj.has_data(TopSeller, user=user, title=category):
                result_file_list.append(obj.instance.result_file)  # 将category 的result_file 加入 result_file_list
                # print(result_file)
            else:
                raise extra_exceptions.ItemDoesNotExist('This category does not exist.')

        if keyword:
            if obj.has_data(Keyword, user=user, title=keyword):
                result_file_list.append(obj.instance.result_file)  # 将keyword的result_file 加入 result_file_list
                # print(result_file)
            else:
                raise extra_exceptions.ItemDoesNotExist('This keyword does not exist.')

        if not result_file_list:
            raise exceptions.ParseError('Please add either a category or a keyword.')

        return Response(result_file_list.__str__(), status=status.HTTP_200_OK)
