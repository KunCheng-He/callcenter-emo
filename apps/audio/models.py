from django.db.models import Model, CharField, ForeignKey, SET_NULL, BooleanField, FloatField
from apps.upload_events.models import UploadEvent
from apps.accounts.models import CustomUser

# Create your models here.

class Audio(Model):
    """音频处理表"""
    orig_file_path = CharField(max_length=256, unique=True, verbose_name='原始音频文件路径')
    left_file_path = CharField(max_length=256, unique=True, verbose_name='音频左声道文件路径')
    right_file_path = CharField(max_length=256, unique=True, verbose_name='音频右声道文件路径')
    upload_event_id = ForeignKey(UploadEvent, on_delete=SET_NULL, null=True, related_name='audio', verbose_name='上传事件')
    checked = BooleanField(default=False, verbose_name='是否已审核')


class AudioPart(Model):
    """ 音频片段表 """
    user_id = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='cut_user', verbose_name='剪辑片段用户')
    cut_audio_path = CharField(max_length=256, unique=False, verbose_name='被剪辑音频文件路径')
    start_time = FloatField(verbose_name='片段开始时间')
    end_time = FloatField(verbose_name='片段结束时间')
    part_path = CharField(max_length=256, null=True, verbose_name='音频片段存储路径')
