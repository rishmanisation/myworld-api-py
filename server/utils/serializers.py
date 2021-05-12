from rest_framework import serializers

from .models import UploadedFileInformation

class UploadedFilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedFileInformation
        fields = ('file_name_hash', 'user_id', 'file_name', 'file_gcp_path', 'file_user_metadata', 'file_hash_crc32c', 'file_hash_md5',
        'file_mime_type', 'file_appl_id', 'file_type', 'file_size', 'file_is_active', 'file_upload_timestamp',)

class FileUploaderSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())
    '''
    class Meta:
        model = FileUploader
        fields = ('file', 'file_description', 'file_user_metadata',)
    '''