from django.db import models
from user.models import AmazonUser
from amazon_analytics.settings import FILE_URL
import os


class TopSeller(models.Model):
    # id,title,create_time,result_file,origin_file,user_id
    user = models.ForeignKey(AmazonUser)
    title = models.CharField(max_length=256, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    result_file = models.FilePathField(path='file/result')
    origin_file = models.FileField(upload_to='file/origin')


### 未知数据库
# class Limit(models.Model):
#     # user_id,keyword_limit,topseller_limit
#     user = models.ForeignKey(AmazonUser)
#     keyword_limit =
#     topseller_limit =
