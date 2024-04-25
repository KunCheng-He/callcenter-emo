from django.db.models import Model, ForeignKey, CASCADE, CharField, SmallIntegerField, FloatField, DateTimeField

from apps.audio.models import AudioPart

# Create your models here.

class DingLabel(Model):
    """ 情感标注表 """
    audio_part_id = ForeignKey(AudioPart, on_delete=CASCADE, null=False, related_name='audio_part_id', verbose_name='音频片段ID')
    audio_role = CharField(max_length=256, unique=False, verbose_name='音频片段所属角色')
    emotion_label = SmallIntegerField(null=False, verbose_name='情感标签')
    text = CharField(max_length=256, unique=False, verbose_name='音频文本内容')
    pleasure = FloatField(null=False, verbose_name='愉悦维评分')
    action = FloatField(null=False, verbose_name='激活维评分')
    ding_time = DateTimeField(auto_now_add=True, verbose_name='标注时间')
