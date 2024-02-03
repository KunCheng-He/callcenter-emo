from django.shortcuts import render
from rest_framework import viewsets

from .models import DingLabel
from .serializers import DingLabelSerializer

# Create your views here.

# 情感标注视图
class DingLabelView(viewsets.ModelViewSet):
    """ 情感标注视图 """
    queryset = DingLabel.objects.all()
    serializer_class = DingLabelSerializer
    http_method_names = ['get', 'post']
