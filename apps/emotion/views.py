from django.shortcuts import render
from rest_framework import viewsets

from .models import Emotion
from .serializers import EmotionSerializer

# Create your views here.


# 情感视图集
class EmotionViewSet(viewsets.ModelViewSet):
    """ 情感视图集 """
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    http_method_names = ['get']
