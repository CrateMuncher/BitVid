import django.http
import django.template
import django.template.loader
from main.models import *

def render_with_context(request, template_name, context_dict={}):
    template = django.template.loader.get_template(template_name)

    if 'login_token' in request.COOKIES:
        user = User.authenticate_token(request.COOKIES["login_token"])
        context_dict['logged_in_user'] = user
    else:
        context_dict['logged_in_user'] = None

    context = django.template.RequestContext(request, context_dict)
    return django.http.HttpResponse(template.render(context))

def get_user(request):
    if 'login_token' in request.COOKIES:
        user = User.authenticate_token(request.COOKIES["login_token"])
        return user
    else:
        return None