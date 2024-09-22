# chat/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Chat, Token
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    list_display = ('username',)
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Chat)
admin.site.register(Token)
