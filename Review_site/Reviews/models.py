from django.db import models
from django.core.validators import validate_image_file_extension, FileExtensionValidator
from django.contrib.auth.models import User

imgvalidator = FileExtensionValidator(allowed_extensions=['jpg'], message='jpg 형식의 확장자만 사용 가능합니다.')

# Create your models here.
class Review_Models(models.Model):
    """
        모델 관련 필드 정의
        
        1. title: 리뷰 제목
        2. ratings: 별점
        3. content: 리뷰 내용
        4. dt_created: 리뷰 작성일자
        5. imgfile: 리뷰 이미지
        6. domain: 도메인 분류 결과
        7. objects: 클래스 분류 결과 -> 여러 개의 오브젝트가 리스트 형태로 반환 가능
        https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
    """
    RATINGS_CHOICES = {
        (1, "★"),
        (2, "★★"),
        (3, "★★★"),
        (4, "★★★★"),
        (5, "★★★★★")
    } # (데이터베이스에 저장되는 값, 웹에 표시되는 값)

    title = models.CharField(max_length=30)
    ratings = models.IntegerField(choices=RATINGS_CHOICES)
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    imgfile = models.ImageField(upload_to='review_images/', validators=[validate_image_file_extension, imgvalidator])
    domain_clf = models.CharField(max_length=15)
    objects_clf = models.CharField(max_length=15)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    viewed_reviews = models.ManyToManyField(Review_Models, related_name='viewed')
