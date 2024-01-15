from rest_framework import serializers
from .models import UploadEvent


# 上传事件序列化
class UploadEventSerializer(serializers.HyperlinkedModelSerializer):
    """ 上传事件序列化 """
    class Meta:
        model = UploadEvent
        fields = ['url', 'cs_user_id', 'upload_time', 'file']
        read_only_fields = ['upload_time',]
    