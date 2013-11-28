from django.template import loader, RequestContext
from django.http import HttpResponse
from main.models import *


def render_with_context(request, template_name, context_dict={}):
    template = loader.get_template(template_name)
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


def home(request):
    return render_with_context(request, "base.html")


def login(request):
    if request.method == "GET":
        return render_with_context(request, "login.html")
    else:
        post_data = request.POST

        user = User.authenticate_credentials(post_data["username"], post_data["password"])
        if user is not None:
            request.set_cookie('login_token', user.login_token)
        else:
            return render_with_context(request, "login.html", {"error": "Invalid username or password."})
