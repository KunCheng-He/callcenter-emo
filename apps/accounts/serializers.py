from rest_framework import serializers
from .models import UserRole, CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

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
        fields = [
            'url', 'email', 'username', 'role', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined',
            'audio_num', 'user_emo_up', 'user_emo_norm', 'user_emo_down', 'emo_up', 'emo_norm', 'emo_down', 'check_num', 'cut_num'
        ]
        read_only_fields = [
            'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined',
            'audio_num', 'user_emo_up', 'user_emo_norm', 'user_emo_down', 'emo_up', 'emo_norm', 'emo_down'
        ]


# Token序列化
class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息

        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token['name'] = user.username
        return token

    def validate(self, attrs):
        """
        此方法为响应数据结构处理
        原有的响应数据结构无法满足需求，在这里重写结构如下：
        {
            "refresh": "xxxx.xxxxx.xxxxx",
            "access": "xxxx.xxxx.xxxx",
            "expire": Token有效期截止时间,
            "username": "用户名",
            "email": "邮箱"
        }

        :param attrs: 請求參數
        :return: 响应数据
        """
        # data是个字典
        # 其结构为：{'refresh': '用于刷新token的令牌', 'access': '用于身份验证的Token值'}
        data = super().validate(attrs)

        # 获取Token对象
        refresh = self.get_token(self.user)
        #加个token的键，值和access键一样
        data['token']=data['access']
        #然后把access键干掉
        del data['access']
        # 令牌到期时间
        data['expire'] = refresh.access_token.payload['exp']  # 有效期
        # 用户名
        data['username'] = self.user.username
        # 邮箱
        data['email'] = self.user.email
        # id
        data['id'] = self.user.id
        return data
