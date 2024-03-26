from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import  Response
from .models import ItemPermissions

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        #if user.is_authenticated:
            #user.is_doctor = validated_token['is_doctor']

        return user


def get_tokens_for_user(user):
    token = RefreshToken.for_user(user)
    #token['is_doctor'] = user.is_doctor
    token = token.access_token
    return token


def grant_admin_rights(user):
    ItemPermissions.objects.create(
        user=user,
        fetch_permission=True,
        list_fetch_permission=True,
        update_permission=True,
        partial_update_permission=True,
        delete_permission=True,
        create_permission=True
    )