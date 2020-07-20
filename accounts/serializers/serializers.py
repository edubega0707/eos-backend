from rest_framework import serializers
from  django.contrib.auth.models import User
from accounts.models import Profile

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



