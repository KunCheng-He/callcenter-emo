from rest_framework import serializers
from .models import DingLabel

# 序列化模型

# 情感标注序列化
class DingLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DingLabel
        fields = ['url', 'audio_part_id', 'audio_role', 'emotion_label', 'text', 'pleasure', 'action', 'ding_time']
