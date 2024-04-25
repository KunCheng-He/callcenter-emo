from django.shortcuts import render
from rest_framework import viewsets
from datetime import datetime

from .models import DingLabel
from .serializers import DingLabelSerializer, DatasetExportSerializer

# Create your views here.

# 情感标注视图
class DingLabelView(viewsets.ModelViewSet):
    """ 情感标注视图 """
    queryset = DingLabel.objects.all()
    serializer_class = DingLabelSerializer
    http_method_names = ['get', 'post']


# 语料导出视图
class ExportView(viewsets.ModelViewSet):
    """ 语料导出视图 """
    queryset = DingLabel.objects.all()
    serializer_class = DatasetExportSerializer
    http_method_names = ['get']

    def get_queryset(self):
        query = DingLabel.objects.all()
        start_time = self.request.query_params.get('startTime', None)
        end_time = self.request.query_params.get('endTime', None)
        
        # 如果提供了startTime和endTime，则匹配在该时间范围内的对象
        if start_time and end_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            query = query.filter(ding_time__range=(start_time, end_time))

        return query
