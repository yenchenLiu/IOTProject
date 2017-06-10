from django.shortcuts import render

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# from .permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import mixins
from rest_framework import permissions, viewsets
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import KeyPairSerializer, UserSerializer, ModelKeyPairSerializer
from django.contrib.auth.models import User
from device.models import UserPublicKey
from Crypto.PublicKey import RSA


# ViewSets define the view behavior.
class UserViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=["get"])
    def get_username(self, request, *args, **kwargs):
        """
            登入後查詢自己的username
        """
        queryset = self.request.user
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)


class KeyPairViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPublicKey.objects.all()
    serializer_class = ModelKeyPairSerializer

    @list_route(methods=["get"])
    def generate_private_key(self, request, *args, **kwargs):
        """
            第一次產生金鑰
        """
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.filter(user=self.request.user).exists():
            if "force" not in kwargs:
                raise serializers.ValidationError({"error": "已產生過鑰匙，如要重新產生參數請呼叫 regenerate_private_key"})
        key = RSA.generate(2048)
        encrypted_key = key.exportKey(pkcs=8, protection = "scryptAndAES128-CBC")
        public_key = key.publickey().exportKey().decode()
        serializer = KeyPairSerializer({"public_key": public_key, "private_key": encrypted_key.decode()})
        key_model = UserPublicKey(user=self.request.user)
        key_model.public_key = public_key
        key_model.save()
        return Response(serializer.data)

    @list_route(methods=["get"])
    def regenerate_private_key(self, request, *args, **kwargs):
        """
            重新產生金鑰
        """
        queryset = self.filter_queryset(self.get_queryset())
        try:
            key_model = queryset.get(user=self.request.user)
        except UserPublicKey.DoesNotExist:
            key_model = UserPublicKey(user=self.request.user)
        key = RSA.generate(2048)
        encrypted_key = key.exportKey(pkcs=8, protection="scryptAndAES128-CBC")
        public_key = key.publickey().exportKey().decode()
        serializer = KeyPairSerializer({"public_key": public_key, "private_key": encrypted_key.decode()})
        key_model.public_key = public_key
        key_model.save()
        return Response(serializer.data)

    @list_route(methods=["post"])
    def get_public_key(self, request):
        """
            使用username 查詢公鑰
            POST username 可取得使用者的公鑰
        """
        queryset = self.filter_queryset(self.get_queryset())
        if "username" not in request.data:
            raise serializers.ValidationError({"username": "請輸入這項參數"})
        try:
            user = User.objects.get(username=request.data["username"])
            key_model = queryset.get(user=user)
        except UserPublicKey.DoesNotExist:
            raise serializers.ValidationError({"error": "使用者尚未啟用"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "沒有這個使用者"})

        serializer = self.get_serializer(key_model)
        return Response(serializer.data)






