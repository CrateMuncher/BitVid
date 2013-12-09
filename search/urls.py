from django.conf.urls import patterns, include, url

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

sqs = SearchQuerySet()


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=SearchView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=ModelSearchForm
    ), name='haystack_search'),
)