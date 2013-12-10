from django.conf.urls import patterns, url
from main.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login', 'main.views.login', name='login'),
    url(r'^signup', 'main.views.signup', name='signup'),
    url(r'^logout', 'main.views.logout', name='logout'),
    url(r'^upload', 'main.views.upload', name='upload'),
    url(r'^video/(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
    url(r'^watch/(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
    url(r'^(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
)
