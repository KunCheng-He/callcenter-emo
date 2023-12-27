from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenViewBase

from .models import UserRole, CustomUser
from .serializers import UserRoleSerializer, UserSerializer, TokenSerializer
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
        request.POST._mutable = True  # 解决请求对象不可更改的问题
        request.data["password"] = make_password(request.data.get("password"))
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """更新用户信息时对password进行加密"""
        request.POST._mutable = True  # 解决请求对象不可更改的问题
        if "password" in request.data:
            request.data["password"] = make_password(request.data.get("password"))
        return super().update(request, *args, **kwargs)


# 自定义的登陆视图
class LoginView(TokenViewBase):
    """登录视图"""
    serializer_class = TokenSerializer  # 使用刚刚编写的序列化类

    # post方法对应post请求，登陆时post请求在这里处理
    def post(self, request, *args, **kwargs):
        # 使用刚刚编写时序列化处理登陆验证及数据响应
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise ValueError(f'验证失败： {e}')
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
