from django.contrib import admin
from .models import *
# Register your models here.

#show the userinfo data more preciesely in admin panel
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['get_user_id', 'get_user_name', 'first_name', 'last_name', 'phone', 'email']

    def get_user_name(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    get_user_name.short_description = 'Username'
    get_user_id.short_description = 'ID'
