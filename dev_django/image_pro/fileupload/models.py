from django.db import models

# Create your models here.
class FileUpload(models.Model):
    # 이미지 필드 -> media 폴더 설정으로 media 폴더에 자동 저장됨.
    # 사용자가 업로드한 경우 데이터를 구분할 수 있는 id 필드가 자동 생성
    imgfile = models.ImageField(null=True, upload_to="", blank=True)