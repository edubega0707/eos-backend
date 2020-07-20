from rest_framework import serializers
from  django.contrib.auth.models import User
from accounts.models import Profile

from accounts.serializers.serializers import (
    UserSerializer,
    ProfileSerializer)
class UserSerializer(serializers.ModelSerializer):
    profile_usuario=ProfileSerializer(many=False)
    class Meta:
        model=User
        fields=['id','username','first_name', 'last_name', 'profile_usuario']

