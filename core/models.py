from django.db import models
from django.contrib.auth.models import User


class TwitchUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.PositiveBigIntegerField(primary_key=True)
    xiv_name = models.CharField(max_length=20)

class OAuth2Token(models.Model):
    name = models.CharField(max_length=40)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_at = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )