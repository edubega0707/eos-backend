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
    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User.objects.create_user(**validated_data)
    #     user.set_password(password) 
    #     user.save() 
    #     return user 

class UserCortoSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountType
        fields='__all__'



