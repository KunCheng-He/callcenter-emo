from rest_framework import serializers
from .models import SERModel

# 序列化模型

# 语音情感识别模型序列化
class SERModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SERModel
        fields = ['url', 'name', 'path']
