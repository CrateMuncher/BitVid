import boto.s3.connection
import boto.s3.key
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
import bitvid.dbinfo
from main.models import *
from main.view_utils import *
import re


def home(request):
    return render_with_context(request, "home.html")


def login(request):
    if request.method == "GET":
        return render_with_context(request, "login.html")
    else:
        post_data = request.POST

        user = User.authenticate_credentials(post_data.get("username", ""), post_data.get("password", ""))
        if user is not None:
            response = HttpResponseRedirect(reverse("home"))
            response.set_cookie('login_token', user.login_token)
            return response
        else:
            return render_with_context(request, "login.html", {"error": "Invalid username or password."})

def signup(request):
    if request.method == "GET":
        return render_with_context(request, "signup.html")
    else:
        post_data = request.POST

        username = post_data.get("username", "")
        password = post_data.get("password", "")
        email = post_data.get("email", "")

        if username == "":
            return render_with_context(request, "signup.html", {"error": "Username must not be empty."})

        if password == "":
            return render_with_context(request, "signup.html", {"error": "Password must not be empty."})

        if email == "":
            return render_with_context(request, "signup.html", {"error": "E-mail must not be empty."})

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            return render_with_context(request, "signup.html", {"error": "Username must only contain letters, numbers and underscores."})

        if not re.match(r'^.{7,}$', password):
            return render_with_context(request, "signup.html", {"error": "Password must be at least 7 characters long."})

        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return render_with_context(request, "signup.html", {"error": "E-mail must be valid."})

        user = User.signup(username, password, email)
        if user is None:
            return render_with_context(request, "signup.html", {"error": "A user with that already exists."})
        user.save()
        return HttpResponseRedirect(reverse("login"))

def logout(request):
    response = HttpResponseRedirect(reverse("login"))
    response.delete_cookie("login_token")
    return response

def view_channel(request, channel):
    pass

def channels(request):
    if get_user(request) is None:
        return HttpResponseRedirect(reverse("login"))

    return render_with_context(request, "channels.html")

def create_channel(request):
    if request.method == "GET":
        if get_user(request) is None:
            return HttpResponseRedirect(reverse("login"))

        return render_with_context(request, "create_channel.html")
    else:
        user = get_user(request)
        name = request.POST.get("name", "")

        if name == "":
            return render_with_context(request, "create_channel.html", {"error": "Name must not be empty."})

        if not re.match(r'^[A-Za-z0-9_-]+$', name):
            return render_with_context(request, "create_channel.html", {"error": "Name must only contain letters, numbers, underscores and hyphens."})

        if Channel.objects.filter(name=name).exists():
            render_with_context(request, "create_channel.html", {"error": "A channel with that name already exists."})

        channel = Channel.objects.create()
        channel.name = name
        channel.members.add(user)
        channel.save()

        return HttpResponseRedirect(reverse("channels"))

def upload(request):
    if request.method == "GET":
        if get_user(request) is None:
            return HttpResponseRedirect(reverse("login"))

        return render_with_context(request, "upload.html")
    else:
        if get_user(request) is None:
            return HttpResponseRedirect(reverse("login"))

        user = get_user(request)
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
        render_with_context(request, "notfound.html", {"error": "Video not found."})

    video = Video.objects.get(pk=video_id)
    return render_with_context(request, "view_video.html", {"video": video})

def notfound(request):
    render_with_context(request, "notfound.html")