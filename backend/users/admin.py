from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
