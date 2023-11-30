from rest_framework import serializers
from .models import UserRole, CustomUser


# 在这里序列化我们的模型

# 用户角色的序列化
class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    """用户角色的序列化"""
    class Meta:
        model = UserRole
        fields = '__all__'

