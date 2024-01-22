from django.shortcuts import render, get_list_or_404
from rest_framework import viewsets

from .models import Audio
from .serializers import AudioSerializer

# Create your views here.

# 音频视图集
class AudioViewSet(viewsets.ModelViewSet):
    """ 音频视图集 """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    http_method_names = ['get']

    def get_queryset(self):
        checked = self.request.query_params.get('checked', None)
        
        # 如果用户提供了 checked 参数，过滤出未审计的样本
        if checked == "True":
            return Audio.objects.filter(checked=True)
        elif checked == "False":
            return Audio.objects.filter(checked=False)
        else:
            return Audio.objects.all()
