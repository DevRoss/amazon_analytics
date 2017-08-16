from django.db import models
from user.models import AmazonUser
from amazon_analytics.settings import FILE_URL
import os


class TopSeller(models.Model):
    # id,title,create_time,result_file,origin_file,user_id
    user = models.ForeignKey(AmazonUser)
    title = models.CharField(max_length=256, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    result_file = models.FilePathField(path='file/top/result')
    origin_file = models.FileField(upload_to='file/top/origin')


class Keyword(models.Model):
    # id,title,create_time,result_file,origin_file,user_id
    user = models.ForeignKey(AmazonUser)
    title = models.CharField(max_length=256, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    result_file = models.FilePathField(path='file/kw/result')
    origin_file = models.FileField(upload_to='file/kw/origin')
