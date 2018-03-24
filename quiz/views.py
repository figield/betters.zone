from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import json
from django.shortcuts import render


def index(request):
    return render(request, 'quiz_index.html', {})


@csrf_protect
def register_new_user(request):
    context = get_default_register_context()
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        context['email'] = json_data.get('email')
        username = json_data.get('name')
        context['username'] = username
        context['exist'] = User.objects.filter(username=username).exists()
        if not request.user.is_anonymous():
            context['login'] = True
            context['login_as'] = request.user.username
        else:
            pass
            # TODO: create temporary user

    return JsonResponse(context)


def get_default_register_context():
    context = dict()
    context['email'] = ''
    context['username'] = ''
    context['exist'] = False
    context['login'] = False
    context['login_as'] = ''
    return context
