from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login', 'main.views.login', name='login'),
    url(r'^signup', 'main.views.signup', name='signup'),
    url(r'^logout', 'main.views.logout', name='logout'),
    url(r'^channels', 'main.views.channels', name='channels'),
    url(r'^create_channel', 'main.views.create_channel', name='create_channel'),
    url(r'^channel/(?P<channel>\w+)', 'main.views.view_channel', name='view_channel'),
    url(r'^upload', 'main.views.upload', name='upload'),
    url(r'^video/(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
    url(r'^watch/(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
    url(r'^(?P<video_id>\d+)', 'main.views.view_video', name='view_video'),
)
