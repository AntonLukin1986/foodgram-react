from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from users.models import Subscribe, User

admin.site.register(Subscribe)
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('username', 'email')
    empty_value_display = '-----'
    readonly_fields = ('first_name', 'last_name')
