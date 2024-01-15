from django.shortcuts import render
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
