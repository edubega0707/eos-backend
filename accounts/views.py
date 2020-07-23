from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from rest_framework import status
from django.http import Http404

from accounts.serializers.nested import(
    UserProfileSerializer,
    UserDetailSerializer,
    AccountSerializer,
    AccountDetailSerializer
)
from accounts.serializers.serializers import(
    UserSerializer,
    AccountTypeSerializer,
    AccountSerializerPost,
    TransactionSerializer
)
from .models import (
    Profile,
    AccountType,
    Account,
    Transaction
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
    permission_classes = [IsAuthenticated, IsAdminUser]
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


# class AccountsListView(generics.ListAPIView):
#     queryset=Account.objects.all()
#     serializer_class=AccountSerializer  
#     filter_backends=[SearchFilter]
#     search_fields=['type_account__id']
#     def get_queryset(self):
#         user=self.request.user
#         return Account.objects.filter(user_account=user.id)


class TypeAccountsView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class MyAccountsView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset            =   Account.objects.all()
    serializer_class    =   AccountSerializerPost
    filter_backends=[SearchFilter]
    search_fields=['type_account__id']
    serializer_action_classes={
        'list':AccountSerializer,
        'retrieve':AccountDetailSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    def get_queryset(self):
        user=self.request.user
        return Account.objects.filter(user_account=user.id)


from django.db.models import F
from django.core import serializers

class DepositoView(APIView):
    def post(self, request, format=None):
        deposito = TransactionSerializer(data=request.data)
        if deposito.is_valid():
            account_id=deposito.validated_data['account']
            deposito_agregar=deposito.validated_data['ammount']
            if(deposito_agregar<0):
                return Response({"error":"El deposito debe ser positivo"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                account=Account.objects.get(id=account_id.id)
                account.ammount=F('ammount')+deposito_agregar
                account.save()
                transaction = Transaction.objects.create(**deposito.validated_data) 
                return Response(deposito.data, status=status.HTTP_201_CREATED)
        return Response(deposito.errors, status=status.HTTP_400_BAD_REQUEST)
        

class WithDrawView(APIView):
    def post(self, request, format=None):
        retiro = TransactionSerializer(data=request.data)
        if retiro.is_valid():
            deposito_retirar=retiro.validated_data['ammount']
            account_id=retiro.validated_data['account']
            account=Account.objects.get(id=account_id.id)
            if(deposito_retirar<0):
                return Response({"error":"El deposito debe ser minimo 1 peso"}, status=status.HTTP_400_BAD_REQUEST)
            elif(deposito_retirar > account.ammount):
                return Response({"error":"El retiro es mayor a tu saldo"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                account.ammount=F('ammount')-deposito_retirar
                account.save()
                transaction = Transaction.objects.create(**retiro.validated_data) 
                return Response(retiro.data, status=status.HTTP_201_CREATED)

        return Response(retiro.errors, status=status.HTTP_400_BAD_REQUEST)
