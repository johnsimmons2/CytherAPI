from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.models import Session


admin.site.register(Session)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass