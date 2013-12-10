from django.conf.urls import patterns, url
from views import ChannelDetailView, ChannelListView,\
    ChannelCreateView

urlpatterns = patterns('',

	url(r'^mine', ChannelListView.as_view(), name='channels'),
    url(r'^create', ChannelCreateView.as_view(), name='create_channel'),
    url(r'^(?P<slug>\w+)', ChannelDetailView.as_view(), name='view_channel')
    )
