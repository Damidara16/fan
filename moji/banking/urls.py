from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'banking'

urlpatterns = [
    url(r'^step1/$', views.number1, name='step1'),
    url(r'^step2/$', views.number2, name='step2'),
    url(r'^step3/$', views.number3, name='step3'),
    url(r'^step/$', views.new, name='step'),
]
