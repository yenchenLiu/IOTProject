from django.conf.urls import url, include

from django.contrib import admin

admin.autodiscover()

from rest_framework import routers
from .views import UserViewSet, MapSiteViewSet


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'site', MapSiteViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
