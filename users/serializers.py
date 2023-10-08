from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'joined_date']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['token_value', 'creation_date', 'delete_date']