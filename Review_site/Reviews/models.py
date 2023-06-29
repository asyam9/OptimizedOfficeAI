from django.db import models
from django.core.validators import validate_image_file_extension, FileExtensionValidator
from django.contrib.auth.models import User

import os
from uuid import uuid4

imgvalidator = FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'], message='다음과 같은 형식의 확장자만 사용 가능합니다(jpg, png, jpeg)')

def rename_imagefile_to_uuid(instance, filename): 	# instance : Feed 모델에서 __str__로 반환해주는 값 현재는 title로 지정
    												# filename : 원본 파일명
    upload_to = f'review_images/' 			        # 파일 저장 위치 설정
    ext = filename.split('.')[-1]        			# 원본 파일명 text.jpg->[text, jpg]로 나누어주고 -1 번째 값만 ext에 담아주기
    uuid = uuid4().hex                   			# 50da5daca34d4802a771047ee463c234 이런 형식에 임의에 이름 생성
    filename = '{}.{}'.format(uuid, ext) 			# '{uuid}.{ext}' -> 50da5daca34d4802a771047ee463c234.jpg
										 			# format(uuid, ext) -> uuid = 파일명, ext = 파일 형식
    return os.path.join(upload_to, filename)		# DB에 저장할 값을 리턴

# Create your models here.
class Review_Models(models.Model):
    """
        모델 관련 필드 정의
        []
        1. title: 리뷰 제목
        2. ratings: 별점
        3. content: 리뷰 내용
        4. dt_created: 리뷰 작성일자
        5. imgfile: 리뷰 이미지
        6. domain: 도메인 분류 결과
        7. objects: 클래스 분류 결과
        https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
    """
    RATINGS_CHOICES = (
        (5, "⭐️⭐️⭐️⭐️⭐️"),
        (4, "⭐️⭐️⭐️⭐️"),
        (3, "⭐️⭐️⭐️"),
        (2, "⭐️⭐️"),
        (1, "⭐️")
     ) # (데이터베이스에 저장되는 값, 웹에 표시되는 값)

    title = models.CharField(max_length=30)
    ratings = models.IntegerField(choices=RATINGS_CHOICES)
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    imgfile = models.ImageField(upload_to=rename_imagefile_to_uuid, validators=[validate_image_file_extension, imgvalidator])
    domain_clf = models.CharField(max_length=15)
    objects_clf = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # yolo 모델 분류 결과를 출력하기 위한 함수 -> 리스트 안 오브젝트를 각각 출력
    def get_objects_list(self):
        if self.objects_clf:
            return self.objects_clf[1:-1].split(', ')
        return []