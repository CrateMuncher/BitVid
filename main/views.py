from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
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

        if not re.match(r'[A-Za-z0-9_]+', username):
            return render_with_context(request, "signup.html", {"error": "Username must only contain letters, numbers and underscores."})

        if not re.match(r'^.{7,}$', password):
            return render_with_context(request, "signup.html", {"error": "Password must be at least 7 characters long."})

        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return render_with_context(request, "signup.html", {"error": "E-mail must be valid."})

        user = User.signup(username, password, email)
        if user is None:
            return render_with_context(request, "signup.html", {"error": "User already exists."})
        user.save()
        return HttpResponseRedirect(reverse("login"))

def logout(request):
    response = HttpResponseRedirect(reverse("login"))
    response.delete_cookie("login_token")
    return response

def upload(request):
    if request.method == "GET":
        return render_with_context(request, "upload.html")

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

        if not re.match(r'[A-Za-z0-9_-]+', name):
            return render_with_context(request, "create_channel.html", {"error": "Name must only contain letters, numbers, underscores and hyphens."})

        channel = Channel.objects.create()
        channel.name = name
        channel.members.add(user)
        channel.save()

        return HttpResponseRedirect(reverse("channels"))