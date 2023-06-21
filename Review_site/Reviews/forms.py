from django.forms import ModelForm
from .models import Review_Models

# 사용자의 데이터를 입력받을 수 있는 양식 ㅡ> 모델 폼 사용
class FileUploadForm(ModelForm):
    class Meta:
        model = Review_Models # 사용할 모델 불러오기
        fields = ['title', 'ratings', 'content', 'imgfile'] # 모델 필드 중 사용자의 입력이 필요한 필드 지정