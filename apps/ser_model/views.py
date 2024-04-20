from rest_framework import viewsets

from .models import SERModel
from .serializers import SERModelSerializer

# Create your views here.

class SERModelViewSet(viewsets.ModelViewSet):
    queryset = SERModel.objects.all()
    serializer_class = SERModelSerializer
    http_method_names = ['get', 'post']
