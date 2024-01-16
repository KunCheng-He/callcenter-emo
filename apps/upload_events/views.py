from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from .models import UploadEvent
from .serializers import UploadEventSerializer
from cc_celery.tasks import tasks

# Create your views here.

class UploadEventView(viewsets.ModelViewSet):
    """ 上传事件视图 """
    queryset = UploadEvent.objects.all()
    serializer_class = UploadEventSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['post', 'get']

    def perform_create(self, serializer):
        # 保存上传事件，并在此进行文件处理逻辑
        serializer.save()
        # 获取已保存的对象实例
        data = serializer.data
        # 调用异步任务，将音频分离加入音频表中
        tasks.audio_process.delay(data)
