from rest_framework import serializers
from  django.contrib.auth.models import User
from accounts.models import Profile, AccountType, Account, Transaction

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =['id','telefono','domicilio', 'foto']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

class UserCortoSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountType
        fields='__all__'

class AccountSerializerPost(serializers.ModelSerializer):
    #type_account=AccountTypeSerializer(many=False, read_only=True)
    class Meta:
        model=Account
        fields='__all__'

class AccountCortoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['id','number_account']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'

