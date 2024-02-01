from django.db.models import Model, ForeignKey, SET_NULL, DateTimeField, FileField
from apps.accounts.models import CustomUser

# Create your models here.

# 上传事件表
class UploadEvent(Model):
    """ 上传事件表 """
    cs_user_id = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='cs_events', verbose_name='客服用户')
    upload_time = DateTimeField(auto_now_add=True, verbose_name='上传时间')
    file = FileField(upload_to='upload_files/%Y/%m/%d', verbose_name='上传文件')
