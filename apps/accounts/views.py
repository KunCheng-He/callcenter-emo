from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.hashers import make_password

from .models import UserRole, CustomUser
from .serializers import UserRoleSerializer, UserSerializer
from .permissions import IsOwnerOrReadCreate

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


# 用户视图集
class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadCreate]

    def create(self, request, *args, **kwargs):
        """重写该方法，注册新用户时对password进行加密"""
        request.data["password"] = make_password(request.data.get("password"))
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """更新用户信息时对password进行加密"""
        if "password" in request.data:
            request.data["password"] = make_password(request.data.get("password"))
        return super().update(request, *args, **kwargs)

