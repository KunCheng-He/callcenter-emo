from django.shortcuts import render
from rest_framework import viewsets

from .models import UserRole
from .serializers import UserRoleSerializer

# Create your views here.

# 用户角色视图集
class UserRoleViewSet(viewsets.ModelViewSet):
    """用户角色视图集"""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
