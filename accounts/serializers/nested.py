from rest_framework import serializers
from  django.contrib.auth.models import User
from accounts.models import Profile,Account,Transaction

from accounts.serializers.serializers import (
    UserSerializer,
    ProfileSerializer,
    AccountTypeSerializer,
    TransactionSerializer
    )
    

class AccountSerializer(serializers.ModelSerializer):
    type_account=AccountTypeSerializer(many=False, read_only=True)
    class Meta:
        model=Account
        fields=['id', 'number_account', 'create_date', 'type_account','ammount']


class TransactionSerializer(serializers.ModelSerializer):
    account=AccountSerializer(many=False, read_only=True)
    class Meta:
        model=Transaction
        fields=['id','user','account','ammount', 'total_account','reference','transaction_date']


class UserProfileSerializer(serializers.ModelSerializer):
    profile_usuario=ProfileSerializer(many=False)
    class Meta:
        model=User
        fields=['id','username','first_name', 'last_name', 'profile_usuario']


class UserDetailSerializer(serializers.ModelSerializer):
    profile_usuario=ProfileSerializer(many=False,read_only=True)
    accounts_user=AccountSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields=['id',
        'username',
        'first_name',
        'last_name',
        'email',
        'profile_usuario',
        'accounts_user'
        ]

class AccountDetailSerializer(serializers.ModelSerializer):
    user_account=UserProfileSerializer(read_only=True)
    type_account=AccountTypeSerializer(many=False, read_only=True)
    account_transaction=TransactionSerializer(many=True, read_only=True)
    class Meta:
        model=Account
        fields=['id', 
        'number_account', 
        'create_date', 
        'type_account',
        'ammount',
        'user_account',
        'account_transaction']


