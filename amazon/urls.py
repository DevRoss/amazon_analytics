from django.conf.urls import url
from .views import AddTopSeller

urlpatterns = [
    url(r'add-topseller$', AddTopSeller.as_view()),
]
