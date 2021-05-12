from django.db import models

# Create your models here.

class UploadedFileInformation(models.Model):
    file_name_hash = models.CharField(primary_key=True,max_length=32)
    user_id = models.CharField(max_length=60)
    file_name = models.CharField(max_length=120)
    file_gcp_path = models.CharField(max_length=120)
    file_user_metadata = models.JSONField()
    file_hash_crc32c = models.CharField(max_length=32)
    file_hash_md5 = models.CharField(max_length=32)
    file_mime_type = models.CharField(max_length=100)
    file_appl_id = models.CharField(max_length=60)
    file_type = models.CharField(max_length=100)
    file_size = models.IntegerField(default=0)
    file_is_active = models.BooleanField()
    file_upload_timestamp = models.DateTimeField(auto_now_add=True)