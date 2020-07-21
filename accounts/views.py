from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import status
from django.http import Http404

from accounts.serializers.nested import(
    UserProfileSerializer,
    UserDetailSerializer
)
from accounts.serializers.serializers import(
    UserSerializer
)
from .models import (
    Profile,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'username':user.username,  
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key,
        })


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class SignUpView(APIView):
    def post(self, request, format=None):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            password=user.validated_data['password']
            newUser = User.objects.create_user(user.validated_data['username'],user.validated_data['email'])
            newUser.set_password(password) 
            newUser.save()
            token, created = Token.objects.get_or_create(user=newUser)
            return Response({
            'user_id': newUser.pk,
            'username': newUser.username, 
            'email':newUser.email, 
            'token': token.key,
        }, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class MyUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        my_user = User.objects.all().get(id=request.user.id)
        serializer = UserDetailSerializer(my_user)
        return Response(serializer.data)