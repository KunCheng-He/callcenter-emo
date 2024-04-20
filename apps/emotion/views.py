from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from datetime import datetime

from .models import Emotion
from .serializers import EmotionSerializer, SERReportSerializer
from apps.audio.models import Audio
from apps.accounts.models import CustomUser

# Create your views here.


# 情感视图集
class EmotionViewSet(viewsets.ModelViewSet):
    """ 情感视图集 """
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        audio_id = self.request.query_params.get('audio', None)
        
        # 如果用户提供了音频ID，过滤出该该音频的情感
        if audio_id:
            audio_instance = get_object_or_404(Audio, id=audio_id)
            return Emotion.objects.filter(audio_id=audio_instance)
        
        # 否则返回所有情感项
        return Emotion.objects.all()


# 质检报告多表视图
class SERReportViewSet(viewsets.ModelViewSet):
    """ 质检报告多表视图 """
    queryset = Emotion.objects.all()
    serializer_class = SERReportSerializer
    http_method_names = ['get']

    def get_queryset(self):
        query = Emotion.objects.all()
        username = self.request.query_params.get('username', None)
        start_time = self.request.query_params.get('startTime', None)
        end_time = self.request.query_params.get('endTime', None)
        
        # 如果提供了username，则过滤出匹配的对象
        if username is not None:
            query = query.filter(audio_id__upload_event_id__cs_user_id__username=username)

        # 如果提供了startTime和endTime，则匹配在该时间范围内的对象
        if start_time and end_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            query = query.filter(audio_id__upload_event_id__upload_time__range=(start_time, end_time))

        return query
    