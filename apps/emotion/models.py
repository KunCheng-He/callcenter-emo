from django.db.models import Model, ForeignKey, SET_NULL, DateTimeField, IntegerField, JSONField
from apps.audio.models import Audio

# Create your models here.

class Emotion(Model):
    """情感存储表"""
    audio_id = ForeignKey(Audio, on_delete=SET_NULL, null=True, related_name='emotion', verbose_name='音频')
    recognition_time = DateTimeField(auto_now_add=True, verbose_name='识别时间')
    frame_num = IntegerField(null=False, verbose_name='分割帧数')
    left_emotions = JSONField(null=False, verbose_name='左声道情感')
    right_emotions = JSONField(null=False, verbose_name='右声道情感')
