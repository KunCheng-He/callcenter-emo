from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import UserRole
from .serializers import UserRoleSerializer

# Create your views here.

# 用户角色视图集
class UserRoleViewSet(viewsets.ModelViewSet):
    """用户角色视图集"""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    def get_permissions(self):
        """重写get_permissions方法，允许管理员增删改，查不受限制"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()
