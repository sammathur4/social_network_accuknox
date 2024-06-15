from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, FriendRequest


class UserAdmin(BaseUserAdmin):
    # Define the fields to be used in displaying the User model.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


# Register the FriendRequest model
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'timestamp', 'accepted')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('accepted', 'timestamp')


admin.site.register(FriendRequest, FriendRequestAdmin)