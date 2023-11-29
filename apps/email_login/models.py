from django.contrib.auth.backends import ModelBackend
from apps.accounts.models import CustomUser

# Create your models here.


class CustomModelBackend(ModelBackend):
    """重写认证方法，改用邮箱登录"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(CustomUser.EMAIL_FIELD)
        if username is None or password is None:
            return
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
