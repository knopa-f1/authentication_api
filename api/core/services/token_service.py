from core.models import UserRefreshToken
from constance import config
from django.utils import timezone
import datetime

import uuid

from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from rest_framework_simplejwt.tokens import AccessToken


class TokenService:
    @staticmethod
    def create_refresh_token(user) -> str:
        # delete all tokens of the user
        UserRefreshToken.objects.filter(user=user).delete()

        # create a new token
        refresh_token = str(uuid.uuid4())
        refresh_token_lifetime = config.REFRESH_TOKEN_LIFETIME
        expires_at = timezone.now() + datetime.timedelta(seconds=refresh_token_lifetime)
        UserRefreshToken.objects.create(user=user, token=refresh_token, expires_at=expires_at)

        return refresh_token

    @staticmethod
    def delete_refresh_token(refresh_token) -> bool:
        try:
            refresh_token = UserRefreshToken.objects.get(token=refresh_token)
            refresh_token.delete()
        except UserRefreshToken.DoesNotExist:
            raise NotFound("No active account found for the given token.")
        except ValueError as e:
            raise e

        return True


    @staticmethod
    def generate_access_token(user):
        token = AccessToken.for_user(user)
        token.set_exp(lifetime=datetime.timedelta(seconds=config.ACCESS_TOKEN_LIFETIME))
        return token

    @staticmethod
    def refresh_access_token(user):
        new_access_token = TokenService.generate_access_token(user)
        return new_access_token

    @staticmethod
    def update_tokens(refresh_token):
        try:
            refresh_token = UserRefreshToken.objects.get(token=refresh_token)

            if refresh_token.expires_at < timezone.now():
                raise AuthenticationFailed("Refresh token expired.")

            user = refresh_token.user
            refresh_token.delete()
            refresh_token = TokenService.create_refresh_token(user)
            access_token = TokenService.refresh_access_token(user)

        except UserRefreshToken.DoesNotExist:
            raise NotFound("No active account found for the given token.")
        except ValueError as e:
            raise e

        return {
            'refresh_token': refresh_token,
            'access_token': str(access_token)
        }




