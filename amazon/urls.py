from django.conf.urls import url
from .views import AddTopSeller, AddKeyword

urlpatterns = [
    url(r'add-topseller$', AddTopSeller.as_view()),
    url(r'add-keyword$', AddKeyword.as_view()),
]
