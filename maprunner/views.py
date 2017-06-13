from django.shortcuts import render

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# from .permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import mixins
from rest_framework import permissions, viewsets
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, MapSiteSerializer
from django.contrib.auth.models import User
from .models import MapSite


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


class MapSiteViewSet(GenericViewSet,
                     mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapSite.objects.all()
    serializer_class = MapSiteSerializer

    @list_route(methods=["get"])
    def get_own_site(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=self.request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["post"])
    def get_other_site(self, request, *args, **kwargs):
        if "lat" not in request.data:
            raise serializers.ValidationError({"lat": "請輸入這項參數"})
        if "long" not in request.data:
            raise serializers.ValidationError({"long": "請輸入這項參數"})
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(user=self.request.user)
        lat = float(request.data["lat"])
        long = float(request.data["long"])
        queryset = queryset.filter(latitude__range=(lat-0.1, lat+0.1), longitude__range=(long-0.1, long+0.1))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)