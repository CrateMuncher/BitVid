import datetime
from haystack import indexes
from channels.models import Channel


class ChannelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True)
    name = indexes.CharField(model_attr='name')
    status = indexes.CharField(model_attr='status')

    def get_model(self):
        return Channel

    def prepare_text(self,obj):
    	return obj.name

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter()