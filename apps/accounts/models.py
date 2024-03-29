from django.db.models import Model, CharField, EmailField, ForeignKey, BooleanField, SET_NULL, DateTimeField, BigIntegerField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils import timezone


# Create your models here.

# 用户角色表
class UserRole(Model):
    """用户角色表"""
    name = CharField(max_length=64, unique=True, verbose_name='角色名称')
    describe = CharField(max_length=256, null=True, blank=True, verbose_name='角色描述')

    def __str__(self):
        return self.name


# 自定义用户
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """自定义用户"""
    email = EmailField(
        max_length=50, null=False, unique=True, verbose_name='用户邮箱',
        error_messages={"unique": "该邮箱地址已经存在"}
    )
    username = CharField(
        max_length=50, null=False, unique=True, verbose_name='用户名',
    )
    role = ForeignKey(UserRole, on_delete=SET_NULL, null=True, related_name='users', verbose_name='用户角色')
    is_staff = BooleanField(
        verbose_name='进入管理后台',
        default=False,
        help_text="指定用户是否可以登录到此管理网站"
    )
    is_active = BooleanField(
        verbose_name='活动用户',
        default=True,
        help_text="指定是否应将此用户视为活动用户。取消选择此项而不是删除帐户"
    )
    date_joined = DateTimeField(default=timezone.now, verbose_name='加入日期')

    # 质检相关字段
    audio_num = BigIntegerField(default=0, null=False, verbose_name='音频数量')
    user_emo_up = BigIntegerField(default=0, null=False, verbose_name='用户正向情感')
    user_emo_norm = BigIntegerField(default=0, null=False, verbose_name='用户中性情感')
    user_emo_down = BigIntegerField(default=0, null=False, verbose_name='用户负向情感')
    emo_up = BigIntegerField(default=0, null=False, verbose_name='客服正向情感')
    emo_norm = BigIntegerField(default=0, null=False, verbose_name='客服中性情感')
    emo_down = BigIntegerField(default=0, null=False, verbose_name='客服负向情感')

    # 核验相关字段
    check_num = BigIntegerField(default=0, null=False, verbose_name='核验音频数量')
    cut_num = BigIntegerField(default=0, null=False, verbose_name='切分音频数量')

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
