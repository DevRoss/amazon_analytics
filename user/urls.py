from django.conf.urls import url
from .views import Login
urlpatterns = [
    url(r'login', Login.as_view()),
]