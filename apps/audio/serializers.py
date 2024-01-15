from rest_framework import serializers
from .models import Audio

# 序列化模型

# 音频序列化
class AudioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Audio
        fields = ['url', 'orig_file_path', 'left_file_path', 'right_file_path', 'upload_event_id']
        read_only_fields = ['upload_event_id']
