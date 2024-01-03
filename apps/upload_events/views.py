from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import UploadEvent
from .serializers import UploadEventSerializer

# Create your views here.

class UploadEventView(CreateAPIView, ListAPIView):
    """ 上传事件视图 """
    queryset = UploadEvent.objects.all()
    serializer_class = UploadEventSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # 保存上传事件，并在此进行文件处理逻辑
        print('serializer:\n', serializer)
        serializer.save()
        print("保存完毕")

    def get_queryset(self):
        return UploadEvent.objects.all()
