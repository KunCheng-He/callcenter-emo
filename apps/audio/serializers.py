from rest_framework import serializers
from .models import Audio, AudioPart

# 序列化模型

# 音频序列化
class AudioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Audio
        fields = ['url', 'orig_file_path', 'left_file_path', 'right_file_path', 'upload_event_id', 'checked']
        read_only_fields = ['upload_event_id']


# 音频片段序列化
class AudioPartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioPart
        fields = ['url', 'user_id', 'cut_audio_path', 'start_time', 'end_time', 'part_path']
