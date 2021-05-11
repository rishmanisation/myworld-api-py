from rest_framework import views, viewsets, status
from rest_framework.response import Response

from google.cloud import storage
from google.cloud.storage import Blob

import hashlib
import crc32c
import json

from .serializers import FileUploaderSerializer, UploadedFilesSerializer
from .models import UploadedFileInformation

client = storage.Client()
bucket = client.get_bucket('rishabh-test-bkt')

class UploadedFilesViewSet(viewsets.ModelViewSet):
    queryset = UploadedFileInformation.objects.all().order_by('file_name')
    serializer_class = UploadedFilesSerializer


class FileUploaderViewSet(viewsets.ViewSet):
    #queryset = FileUploader.objects.all()
    serializer_class = FileUploaderSerializer

    def create(self, request):
        if 'files' not in request.FILES:
            print(request.FILES)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        responses = []
        files = request.FILES.getlist('files')
        metadata = json.loads(request.data['metadata'])
        index = 0
        for file in files:
            file_name = file.name
            file_type = file.content_type

            file_dir = request.data['appliance']
            if 'image' in file_type:
                file_dir += '/image/'
            elif file_type == 'application/pdf':
                file_dir += '/pdf/'
            elif file_type == 'application/msword' or file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                file_dir += '/document/'
            elif file_type == 'application/vnd.ms-excel' or file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                file_dir += '/spreadsheet/'
            
            file_gcp_path = 'rish.ananthan@yash.com/' + file_dir + file_name
            file_name_hash = hashlib.md5(file_gcp_path.encode('utf-8')).hexdigest()
            
            file_size = file.size
            file_user_metadata = metadata[index]
            file_hash_md5 = hashlib.md5(file.read()).hexdigest()
            file_hash_crc32c = crc32c.crc32c(file.read())
            ufi = UploadedFileInformation.objects.create(file_name_hash=file_name_hash, user_id='rish.ananthan@yash.com', file_name=file_name,
                                        file_gcp_path=file_gcp_path, file_user_metadata=file_user_metadata, file_hash_crc32c=file_hash_crc32c, file_hash_md5=file_hash_md5,
                                        file_type=file_type, file_size=file_size, file_is_active=True)
            responses.append(ufi)

            blob = Blob(file_gcp_path + file_name, bucket)
            blob.metadata = file_user_metadata
            blob.upload_from_file(file, rewind=True)
            index += 1
        
        return Response(status=status.HTTP_201_CREATED)

