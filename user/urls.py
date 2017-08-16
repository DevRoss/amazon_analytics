from django.conf.urls import url
from .views import Login, Logout

urlpatterns = [
    url(r'login', Login.as_view()),
    url(r'logout', Logout.as_view()),
]
