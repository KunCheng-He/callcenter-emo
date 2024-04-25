from rest_framework import serializers
from .models import DingLabel

# 序列化模型

# 情感标注序列化
class DingLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DingLabel
        fields = ['url', 'audio_part_id', 'audio_role', 'emotion_label', 'text', 'pleasure', 'action', 'ding_time']


# 剪辑导出序列化
class DatasetExportSerializer(serializers.HyperlinkedModelSerializer):
    # 额外信息
    audio_path = serializers.CharField(source="audio_part_id.part_path")

    class Meta:
        model = DingLabel
        fields = ['audio_path', 'audio_role', 'emotion_label', 'text', 'pleasure', 'action', 'ding_time']
