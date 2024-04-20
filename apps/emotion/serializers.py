from rest_framework import serializers
from .models import Emotion

from apps.accounts.models import CustomUser
from apps.upload_events.models import UploadEvent
from apps.audio.models import Audio

# 序列化模型

# 情感序列化
class EmotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Emotion
        fields = ['url', 'audio_id', 'recognition_time', 'frame_num', 'left_emotions', 'right_emotions']
        read_only_fields = ['audio_id']


# 多表关联序列化
class SERReportSerializer(serializers.ModelSerializer):
    # 其它字段
    orig_file_path = serializers.CharField(source="audio_id.orig_file_path")
    left_file_path = serializers.CharField(source="audio_id.left_file_path")
    right_file_path = serializers.CharField(source="audio_id.right_file_path")
    upload_time = serializers.DateTimeField(source="audio_id.upload_event_id.upload_time")
    username = serializers.CharField(source="audio_id.upload_event_id.cs_user_id.username")

    class Meta:
        model = Emotion
        fields = [
            "frame_num", "left_emotions", "right_emotions", "orig_file_path", "left_file_path", "right_file_path",
            "upload_time", "username"
        ]
