from tokenize import TokenError

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthHelper:

    @staticmethod
    def login_success_response(user_instance, request):
        token, refresh_token = user_instance.get_tokens()
        data = {
            "access_token": token,
            "refresh_token": refresh_token,
        }
        return data

    @staticmethod
    def blacklist_token(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise ValidationError({"message": 'Token is blacklisted'})
