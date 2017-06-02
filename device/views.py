from django.shortcuts import render

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
# from .permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer
from django.contrib.auth.models import User, Group


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['read']
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # TokenHasScope
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
