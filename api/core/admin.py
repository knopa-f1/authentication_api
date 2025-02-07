from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserRefreshToken

admin.site.register(User, UserAdmin)


@admin.register(UserRefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

