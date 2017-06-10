from django.contrib import admin
from device.models import UserPublicKey
# Register your models here.

@admin.register(UserPublicKey)
class SettingOptionsAdmin(admin.ModelAdmin):
    list_display = ('user',)