from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserRefreshToken

admin.site.register(User, UserAdmin)
admin.site.site_header = "RESTful API for Authentication admin webpage"
admin.site.site_title = "RESTful API for Authentication admin webpage"


@admin.register(UserRefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
