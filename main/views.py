import boto.s3.connection
import boto.s3.key
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import TemplateView, CreateView, DetailView
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,\
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import bitvid.dbinfo
from main.models import *
from main.view_utils import get_user
import re

#Used to mix in login required behavior to class based views
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    #View to handle the home page
    template_name = "home.html"

class NotFoundView(TemplateView):
    template_name = "notfound.html"

def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        post_data = request.POST
        username = post_data.get("username")
	password = post_data.get("password")
	user = authenticate(username=post_data.get("username", ""), password=post_data.get("password",""))
        if user is not None:
	    auth_login(request,user)
            response = HttpResponseRedirect(reverse("home"))
            return response
        else:
            return render(request,"login.html", {"error": "Invalid username or password."})

def signup(request):
    if request.method == "GET":
        return render(request,"signup.html")
    else:
        post_data = request.POST

        username = post_data.get("username", "")
        password = post_data.get("password", "")
        email = post_data.get("email", "")

        if username == "":
            return render(request, "signup.html", {"error": "Username must not be empty."})

        if password == "":
            return render(request, "signup.html", {"error": "Password must not be empty."})

        if email == "":
            return render(request, "signup.html", {"error": "E-mail must not be empty."})

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            return render(request, "signup.html", {"error": "Username must only contain letters, numbers and underscores."})

        if not re.match(r'^.{7,}$', password):
            return render(request, "signup.html", {"error": "Password must be at least 7 characters long."})

        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return render(request, "signup.html", {"error": "E-mail must be valid."})

        user = User.signup(username, password, email)
        if user is None:
            return render(request, "signup.html", {"error": "A user with that already exists."})
        user.save()
        return HttpResponseRedirect(reverse("login"))

def logout(request):
    auth_logout(request) 
    response = HttpResponseRedirect(reverse("login"))
    return response

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

@login_required
def upload(request):
    if request.method == "GET":

        return render(request, "upload.html")
    else:

        user = request.user
        file = request.FILES.get("file", None)

        if file is None:
            return HttpResponseBadRequest("You did not pass a file.")

        title = request.POST.get("title", "")
        desc = request.POST.get("desc", "")
        channel_id_str = request.POST.get("channel", "1")

        try:
            channel_id = int(channel_id_str)
        except ValueError:
            return HttpResponseBadRequest("Channel ID must be an integer")

        if title == "":
            return HttpResponseBadRequest("Title must not be empty.")

        if not re.match(r'^.{0,2000}$', title):
            return HttpResponseBadRequest("Description must not be longer than 2000 characters.")

        if not Channel.objects.filter(pk=channel_id).exists():
            return HttpResponseBadRequest("Channel ID must be a valid channel.")

        channel = Channel.objects.get(pk=channel_id)

        if not channel.members.filter(id=user.id).exists():
            return HttpResponseBadRequest("You do not own that channel.")


        video = Video.objects.create(uploader=user)
        video.title = title
        video.desciption = desc
        video.channel = channel
        video.save()

        video_file = VideoFile.objects.create()
        video_file.save()
        video_file.format = file.content_type

        video.video_files.add(video_file)

        video_file.save()
        video.save()

        conn = boto.s3.connection.S3Connection(bitvid.dbinfo.AWS_ACCESS, bitvid.dbinfo.AWS_SECRET)

        bucket = conn.get_bucket("bitvid-video")
        bucket.set_acl("public-read")
        key = boto.s3.key.Key(bucket)

        video_path = str(video.id) + "/" + "original.mp4"

        video_file.url = "http://d6iy9bzn1qbz8.cloudfront.net/" + video_path

        key.key = video_path
        key.set_contents_from_filename(file.temporary_file_path())

        key.set_acl('public-read')

        conn.close()

        video_file.save()
        return HttpResponse(str(video.id))

def view_video(request, video_id):
    if not Video.objects.filter(pk=video_id).exists():
        render(request, "notfound.html", {"error": "Video not found."})

    video = Video.objects.get(pk=video_id)
    return render(request, "view_video.html", {"video": video})

