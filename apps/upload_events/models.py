from django.db.models import Model, ForeignKey, SET_NULL, DateTimeField, FileField
from apps.accounts.models import CustomUser
from apps.ser_model.models import SERModel

# Create your models here.

# 上传事件表
class UploadEvent(Model):
    """ 上传事件表 """
    cs_user_id = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='cs_events', verbose_name='客服用户')
    ser_model_id = ForeignKey(SERModel, on_delete=SET_NULL, null=True, related_name='ser_model', verbose_name='语音情感识别模型')
    upload_time = DateTimeField(auto_now_add=True, verbose_name='上传时间')
    file = FileField(upload_to='upload_files/%Y/%m/%d', verbose_name='上传文件')
