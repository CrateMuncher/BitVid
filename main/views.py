from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
import re


def render_with_context(request, template_name, context_dict={}):
    template = loader.get_template(template_name)

    if 'login_token' in request.COOKIES:
        user = User.authenticate_token(request.COOKIES["login_token"])
        context_dict['logged_in_user'] = user
    else:
        context_dict['logged_in_user'] = None

    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))

def home(request):
    return render_with_context(request, "base.html")


def login(request):
    if request.method == "GET":
        return render_with_context(request, "login.html")
    else:
        post_data = request.POST

        user = User.authenticate_credentials(post_data.get("username", ""), post_data.get("password", ""))
        if user is not None:
            response = HttpResponseRedirect("/")
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

        if not re.match(r'[A-Za-z0-9-]+', username):
            return render_with_context(request, "signup.html", {"error": "Username must only contain letters, numbers and underscores."})

        if not re.match(r'^.{7,}$', password):
            return render_with_context(request, "signup.html", {"error": "Password must be at least 7 characters long."})

        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return render_with_context(request, "signup.html", {"error": "E-mail must be valid."})

        user = User.signup(username, password, email)
        if user is None:
            return render_with_context(request, "signup.html", {"error": "User already exists."})
        user.save()
        return HttpResponseRedirect("/login")

def logout(request):
    response = HttpResponseRedirect("/login")
    response.delete_cookie("login_token")
    return response