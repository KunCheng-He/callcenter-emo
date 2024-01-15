from django.db.models import Model, CharField, ForeignKey, SET_NULL
from apps.upload_events.models import UploadEvent

# Create your models here.

class Audio(Model):
    """音频处理表"""
    orig_file_path = CharField(max_length=256, unique=True, verbose_name='原始音频文件路径')
    left_file_path = CharField(max_length=256, unique=True, verbose_name='音频左声道文件路径')
    right_file_path = CharField(max_length=256, unique=True, verbose_name='音频右声道文件路径')
    upload_event_id = ForeignKey(UploadEvent, on_delete=SET_NULL, null=True, related_name='audio', verbose_name='上传事件')
