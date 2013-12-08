from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Channel
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

# Create your views here.
@login_required
def channels(request):
    
    return render(request, "channels.html")

@login_required
def create_channel(request):
    if request.method == "GET":

        return render(request, "create_channel.html")
    else:
        user = request.user
        name = request.POST.get("name", "")

        channel = Channel(name=name)
        try:
            channel.save()
            channel.members.add(user) # Channel needs to be saved before we can add a relationshp
            channel.full_clean() # validate
            channel.save()

        except IntegrityError: #
            return render(request, "create_channel.html",{"error":"Channel with this name already exists"})

        except ValidationError, e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            return render(request, "create_channel.html",{"error":non_field_errors})
        
        return HttpResponseRedirect(reverse("channels"))

def view_channel(request, channel):
    ch = Channel.objects.get(name=channel)
    return render(request, "view_channel.html", {"channel": ch})