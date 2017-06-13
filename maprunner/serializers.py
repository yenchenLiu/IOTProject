from rest_framework import serializers
from django.contrib.auth.models import User
from maprunner.models import MapSite

# first we define the serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class MapSiteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    class Meta:
        model = MapSite
        fields = "__all__"
