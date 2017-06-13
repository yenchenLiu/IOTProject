from django.contrib import admin
from maprunner.models import MapSite
# Register your models here.


@admin.register(MapSite)
class MapSiteAdmin(admin.ModelAdmin):
    list_display = ('user',)
