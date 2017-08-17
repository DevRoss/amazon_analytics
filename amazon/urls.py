from django.conf.urls import url
from .views import AddTopSeller, GetTimeTop, AddKeyword, GetAmazonList

urlpatterns = [
    url(r'add-topseller$', AddTopSeller.as_view()),
    url(r'add-keyword$', AddKeyword.as_view()),
    url(r'get-topseller$', GetTimeTop.as_view()),
    url(r'get-topseller$', GetTimeTop.as_view()),
    url(r'get-amazonlist$', GetAmazonList.as_view()),
]
