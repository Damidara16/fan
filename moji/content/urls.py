from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'content'

urlpatterns = [
    url(r'^detail/(?P<id>[0-9]+)/$', views.detailContent, name='detail'),
#post create
    url(r'^create/post/$', views.postCreate.as_view(), name='CreatePost'),
#video create
    url(r'^create/video/$', views.videoCreate.as_view(), name='CreateVideo'),
#tweet create
    url(r'^create/tweet/$', views.tweetCreate.as_view(), name='CreateTweet'),
#delete content
    url(r'^delete/(?P<id>[0-9]+)/$', views.deleteContent, name='DeleteContent'),
#comment create
    url(r'^create/comment/(?P<pk>[0-9]+)/$', views.commentCreate, name='CreateComment'),

#list content, clickable for detail
#detail view with comments listed on the content
]
