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
        print("序列化数据:\n", data)
    
    def get_queryset(self):
        # 暂时利用该请求测试一下异步任务的执行
        tasks.test_task.delay()
        return UploadEvent.objects.all()
