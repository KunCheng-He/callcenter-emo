from rest_framework import serializers
from .models import Emotion

# 序列化模型

# 情感序列化
class EmotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Emotion
        fields = ['url', 'audio_id', 'recognition_time', 'frame_num', 'left_emotions', 'right_emotions']
        read_only_fields = ['audio_id']
