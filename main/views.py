
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import TemplateView, CreateView, DetailView
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from main.models import *
from channels.models import Channel
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

"""def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                response = HttpResponseRedirect(reverse("home"))
                return response
            else:
                return render(request,"login.html", {"error": "Account suspended"})
        else:
            return render(request,"login.html", {"error": "Invalid username or password."})"""

def signup(request):
    if request.method == "GET":
        return render(request,"registration/signup.html")
    else:
        post_data = request.POST

        username = post_data.get("username", "")
        password = post_data.get("password", "")
        email = post_data.get("email", "")

        if username == "":
            return render(request, "registration/signup.html", {"error": "Username must not be empty."})

        if password == "":
            return render(request, "registration/signup.html", {"error": "Password must not be empty."})

        if email == "":
            return render(request, "registration/signup.html", {"error": "E-mail must not be empty."})

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            return render(request, "registration/signup.html", {"error": "Username must only contain letters, numbers and underscores."})

        if not re.match(r'^.{7,}$', password):
            return render(request, "registration/signup.html", {"error": "Password must be at least 7 characters long."})

        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return render(request, "registration/signup.html", {"error": "E-mail must be valid."})

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, "registration/signup.html", {"error": "A user with that username already exists."})
        user.save()
        return HttpResponseRedirect(reverse("login"))

def logout(request):
    auth_logout(request) 
    response = HttpResponseRedirect(reverse("login"))
    return response