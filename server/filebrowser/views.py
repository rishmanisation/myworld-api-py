from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from utils.models import UploadedFileInformation
from .serializers import FileBrowserSerializer

# Create your views here.
class FileBrowserViewSet(viewsets.ModelViewSet):
    #queryset = UploadedFileInformation.objects.all().order_by('file_name'
    serializer_class = FileBrowserSerializer

    def get_queryset(self):
        queryset = UploadedFileInformation.objects.all()
        file_appl_id = self.request.query_params.get('appl_id')
        if file_appl_id is not None:
            queryset = queryset.filter(file_appl_id=file_appl_id)
        return queryset