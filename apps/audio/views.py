import os
from django.shortcuts import render
from django.http import FileResponse, HttpResponseNotFound
from django.views import View
from rest_framework import viewsets


from .models import Audio, AudioPart
from .serializers import AudioSerializer, AudioPartSerializer

# Create your views here.

# 音频视图集
class AudioViewSet(viewsets.ModelViewSet):
    """ 音频视图集 """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        checked = self.request.query_params.get('checked', None)
        
        # 如果用户提供了 checked 参数，过滤出未审计的样本
        if checked == "True":
            return Audio.objects.filter(checked=True)
        elif checked == "False":
            return Audio.objects.filter(checked=False)
        else:
            return Audio.objects.all()
    

# 音频文件获取视图
class AudioFileView(View):
    """ 音频文件获取视图 """

    def get(self, request):
        path = self.request.GET.get('path', None)
        file_path = os.path.join(os.getcwd(), path[1:])
        try:
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'audio/mpeg'
            return response
        except:
            return HttpResponseNotFound("文件不存在")


# 音频片段视图
class AudioPartView(viewsets.ModelViewSet):
    """ 音频片段视图 """
    queryset = AudioPart.objects.all()
    serializer_class = AudioPartSerializer
    http_method_names = ['get', 'post']
