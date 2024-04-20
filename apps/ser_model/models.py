from django.db.models import Model, CharField, FileField

# Create your models here.

class SERModel(Model):
    """ 语音情感识别模型 """
    name = CharField(max_length=256, unique=True, verbose_name='模型名称')
    path = FileField(upload_to='ser_models', verbose_name='语音情感识别模型文件')
