from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index ,name='home'),
    url(r'^bug/$', views.emailReport.as_view(), name='bug'),
    url(r'^search/$', views.SearchUser, name='search')

]
