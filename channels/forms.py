from channels.models import Channel
from django.forms import ModelForm
from django import forms

class ChannelForm(ModelForm):

    class Meta:
        model = Channel
        fields = ["name"]
