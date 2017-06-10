from rest_framework import serializers
from django.contrib.auth.models import User
from device.models import UserPublicKey


# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ModelKeyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPublicKey
        fields = ['public_key']


class KeyPairSerializer(serializers.Serializer):
    public_key = serializers.ReadOnlyField()
    private_key = serializers.ReadOnlyField()
