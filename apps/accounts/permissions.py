from rest_framework.permissions import BasePermission


# 自定义权限

class IsOwnerOrReadCreate(BasePermission):
    """只允许对象拥有者进行修改，其余只能读和创建"""
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'POST'):
            return True
        return obj.id == request.user.id