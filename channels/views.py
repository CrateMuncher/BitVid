from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Channel
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import TemplateView, CreateView, DetailView

from main.views import LoginRequiredMixin
from channels.forms import ChannelForm

class ChannelDetailView(DetailView):
    #A view for when users look for a single Channel
    model = Channel #Tells the DetailView to use the Channel model
    template_name = "view_channel.html" 
    context_object = "channel" #Sets the name in the template context

    #Sets the field to use for lookups; in this case the name field
    slug_field = "name"


class ChannelListView(LoginRequiredMixin, TemplateView):
    #A view for when users look at all channels
    template_name = "channels.html"


class ChannelCreateView(LoginRequiredMixin, CreateView):
    template_name = "create_channel.html"
    model = Channel
    form_class = ChannelForm

    def post(self, request, *args, **kwargs):
        #We need to set this for the Channel.members field
        self.user = request.user
        return super(ChannelCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        #self.form_valid = True #Needed so we know later we have a valid object
        self.object = form.save()
        self.object.members.add(self.user)
        self.object.save()

        return super(ChannelCreateView, self).form_valid(form)