import pyotp
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, FetchSerializer, ItemPermissionsSerializer
from .models import CustomUser, ItemPermissions
from .permissions import IsSuperuser


class RegistrationView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        if 'email' not in request.data:  # or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']

        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_data = (AccessToken.for_user(user))
            auth_data.payload['email'] = user.email
            return Response({'msg': str(auth_data)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class UpdateProfileRoleView(APIView):
    """
    View for changing user's role and permissions
    """
    permission_classes = (IsSuperuser,)

    def post(self, request):
        if 'email' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        #changing user's role and permissions
        role = request.POST['role']

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'msg': 'Cannot find user with such credentials'}, status=status.HTTP_400_BAD_REQUEST)
        user.user_role = role
        user_permissions, _ = ItemPermissions.objects.get_or_create(user=user)
        if role == "MANAGER":
            user_permissions.create_permission = True
            user_permissions.save()
        if role == "ADMIN":
            user_permissions.update_permission = True
            user_permissions.partial_update_permission = True
            user_permissions.create_permission = True
            user_permissions.delete_permission = True
            user_permissions.save()
        return Response({'msg': 'User profile successfully updated'}, status=status.HTTP_200_OK)


class RetrieveUpdateItemPermissionsAPIView(generics.RetrieveUpdateAPIView):
    """
    View for manual changing users permissions
    """
    queryset = ItemPermissions.objects.all()
    permission_classes = (IsSuperuser,)
    serializer_class = ItemPermissionsSerializer


class FetchProfileView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = FetchSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.get_user_data(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
