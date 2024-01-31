from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from .models import OAuth2Token, TwitchUser

class TwitchBackend(BaseBackend):
    def authenticate(self, request, twitch_user=None, token=None):
        oauth = OAuth()
        oauth.register('twitch')
        

        #have local user?
        try:
            t_user = TwitchUser.objects.get(id=twitch_user['id'])
            user = t_user.user
            user.username = twitch_user['login']
            user.save()
            
            local_token = OAuth2Token.objects.get(user=user)
            local_token.access_token = token['access_token']
            local_token.refresh_token = token['refresh_token']
            local_token.expires_at = token['expires_at']
            local_token.save()

            return user

        #no local user
        except TwitchUser.DoesNotExist:
            #create local user
            user = User.objects.create_user(twitch_user['login'])
            user.save()

            new_twitch_user = TwitchUser()
            new_twitch_user.id = twitch_user['id']
            new_twitch_user.user = user
            new_twitch_user.save()

            #save token
            new_token = OAuth2Token()
            new_token.user = user
            new_token.token_type = token['token_type']
            new_token.access_token = token['access_token']
            new_token.refresh_token = token['refresh_token']
            new_token.expires_at = token['expires_at']
            new_token.save()

            return user

        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None