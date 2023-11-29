from django.contrib import admin
from .models import UserRole, CustomUser

# Register your models here.


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色管理"""
    list_display = ["name", "describe"]
    search_fields = list_display


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """用户管理"""
    list_display = ["email", "username", "role", "is_staff", "is_active", "date_joined"]
    search_fields = ["email", "username"]
    list_filter = ["role", "is_staff", "is_active"]
