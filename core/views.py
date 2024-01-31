from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from .models import OAuth2Token, TwitchUser

from authlib.integrations.django_client import OAuth

from django.contrib.auth.decorators import login_required
import requests
import re

oauth = OAuth()
oauth.register(
    name='twitch',
    token_endpoint_auth_method='client_secret_post'
)
twitch_client_headers = {
   'Client-Id': settings.AUTHLIB_OAUTH_CLIENTS['twitch']['client_id']
}


lodestone_search_base = 'https://na.finalfantasyxiv.com/lodestone/character/'

def index(request):
    context = {
        'title': 'Twitch Chat Names to FFXIV Names'
    }
    if request.user.is_authenticated:
        return render(request, 'core/setup.html', context)

    else:

        return render(request, 'core/index.html', context)

def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'core/about.html', context)

def twitch_login(request):
    redirect_to = request.build_absolute_uri('/authorize/')
    return oauth.twitch.authorize_redirect(request, redirect_to)


def authorize(request):
    token = oauth.twitch.authorize_access_token(request)
    resp = oauth.twitch.get('users', token=token, headers=twitch_client_headers)
    twitch_response = resp.json()
    if len(twitch_response['data']) == 1:
        twitch_user = twitch_response['data'][0]
        user = authenticate(twitch_user=twitch_user, token=token)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('not authorized')
    context = {
        'title': 'Authorization'
    }
    return render(request, 'core/index.html', context)


def twitch_logout(request):
  logout(request)
  context = {
    'title': 'Logged Out'
  }
  return HttpResponseRedirect("/")

@login_required
def delete_user(request):
  user = request.user
  user.delete()
  
  logout(request)
  return HttpResponseRedirect("/")

@login_required
def lodestone_search(request, world, name):
    search_url = f'{lodestone_search_base}?q={name}&worldname={world}'
    search_result = requests.get(search_url)
    response = HttpResponse(search_result.text)
    return response

@login_required
def lodestone_check(request, id):
    search_url = f'{lodestone_search_base}{id}/'
    r = requests.get(search_url)
    m = re.search(r'<title>(.*)\s\|.*</title>', r.text)
    xiv_name = m.group(1).strip()
    request.user.twitchuser.xiv_name = xiv_name
    request.user.twitchuser.save()

    response_data = {
       'xiv_name': request.user.twitchuser.xiv_name
    }
    response = JsonResponse(response_data)
    return response


    
def users_endpoint(request, twitch_id):
    try:
        user = User.objects.get(username = twitch_id)
        if user.twitchuser.xiv_name != "":
            user_data = {
                "twitch_id": user.twitchuser.id,
                "twitch_name": user.username,
                "xiv_name": user.twitchuser.xiv_name
            }
            response = JsonResponse(user_data)
        else:
            response = JsonResponse({})
    except User.DoesNotExist:
        response = JsonResponse({})
        
    response["Access-Control-Allow-Origin"] = "*"
    response["Cache-Control"] = "public, max-age=300, must-revalidate"
    return response
