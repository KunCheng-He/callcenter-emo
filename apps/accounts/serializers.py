from rest_framework import serializers
from .models import UserRole, CustomUser


# 在这里序列化我们的模型

# 用户角色的序列化
class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    """用户角色的序列化"""
    class Meta:
        model = UserRole
        fields = '__all__'


# 用户信息序列化
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """用户信息序列化"""
    class Meta:
        model = CustomUser
        fields = ['url', 'email', 'username', 'role', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined']
        read_only_fields = ['is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined']
    