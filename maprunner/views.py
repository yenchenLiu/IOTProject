from math import radians, cos, sin, asin, sqrt

from django.shortcuts import render

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
        queryset = queryset.filter(latitude__range=(lat-0.01, lat+0.01), longitude__range=(long-0.01, long+0.01))

        exclude_site_id = []
        for item in queryset:
            if MapSiteViewSet._haversine(item.longitude, item.latitude, long, lat) > 0.2:
                exclude_site_id.append(item.id)
        queryset = queryset.exclude(id__in=exclude_site_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def _haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r