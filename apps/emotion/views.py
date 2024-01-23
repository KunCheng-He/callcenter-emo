from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from .models import Emotion
from .serializers import EmotionSerializer
from apps.audio.models import Audio

# Create your views here.


# 情感视图集
class EmotionViewSet(viewsets.ModelViewSet):
    """ 情感视图集 """
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        audio_id = self.request.query_params.get('audio-id', None)
        
        # 如果用户提供了音频ID，过滤出该该音频的情感
        if audio_id:
            audio_instance = get_object_or_404(Audio, id=audio_id)
            return Emotion.objects.filter(audio_id=audio_instance)
        
        # 否则返回所有情感项
        return Emotion.objects.all()
