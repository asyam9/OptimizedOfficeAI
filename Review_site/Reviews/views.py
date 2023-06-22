from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from Reviews.models import Review_Models
from .forms import FileUploadForm

import tensorflow as tf
from tensorflow.keras.preprocessing import image

from ultralytics import YOLO

import time
import simplejson as json

class IndexView(ListView):
    """리뷰 조회 페이지"""
    model = Review_Models
    template_name = 'Reviews/index.html'
    context_object_name = 'reviews'
    paginate_by = 4 # 한 페이지에 표현할 개수
    ordering = ['-dt_created'] # 순서(- 내림차순)

    def index(self, request):
        reviews = self.model.objects.all()
        return render(request, self.template_name, {'reviews':reviews})

# 리뷰 작성 페이지 로직
def upload(request):
    ### 사용자가 폼을 통해 입력을 했을 경우, 
    if request.method == 'POST':

        # 입력값 받아오기
        title = request.POST['title']
        ratings = request.POST['ratings']
        content = request.POST['content']
        img = request.FILES["imgfile"]

        # 새로운 데이터 생성
        new_file = Review_Models(
            title = title,
            ratings = ratings,
            content = content,
            imgfile = img
        )

        # 입력받은 데이터를 데이터베이스에 저장 -> 자동으로 id 생성
        new_file.save()

        # 결과보기 페이지에 id 값 같이 넘겨주기
        return redirect('detail', post_id=new_file.id)
    
    ### 사용자가 입력하기 전, 폼을 화면에 출력해주는 것
    else:
        fileuploadForm = FileUploadForm()
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'Reviews/review_upload.html', context)

# 이미지 도메인 분류 로직
def img_domain_clf(img_url):
    # 이미지 경로 설정(받아온 url과 로컬 환경의 경로 합쳐주기)
    path = "C:/Users/DaonWoori/programming/OptimizedOfficeAI/Review_site" + img_url
    print(path)

    # 이미지 불러오기
    img = image.load_img(path, target_size=(224, 224))

    # 이미지 전처리
    img = image.img_to_array(img)
    img = img / 255.0
    img = tf.expand_dims(img, axis=0)

    # AI 모델 로드
    model = tf.keras.models.load_model('C:/Users/DaonWoori/programming/OptimizedOfficeAI/Review_site/ai_models/model_16.h5', compile=False)
    
    # 이미지 분류 수행
    start_time = time.time()
    prediction = model.predict(img)
    end_time = time.time()

    diff_time = end_time - start_time

    # 분류 결과 반환 -> 수행 시간 소수점 4자리까지만 반환
    result = prediction[0][0]
    if result > 0.5:
        domain = 'Office'
    else:
        domain = 'None Office'
    return domain, round(diff_time, 4)

# 이미지 클래스 분류 로직
def img_object_clf(img_url):
    # 이미지 경로 설정(받아온 url과 로컬 환경의 경로 합쳐주기)
    path = "C:/Users/DaonWoori/programming/OptimizedOfficeAI/Review_site" + img_url

    # 모델 불러오기 
    model = YOLO("C:/Users/DaonWoori/programming/OptimizedOfficeAI/Review_site/ai_models/best.pt")
    names = model.names

    # 이미지 분류 수행
    start_time = time.time()
    # results = model(path, save=True)
    result = model.predict(source=path)
    end_time = time.time()

    diff_time = end_time - start_time

    objects_list = []

    for r in result:
        for c in r.boxes.cls:
            objects_list.append(names[int(c)])

    print(objects_list)
    objects_str = json.dumps(objects_list)

    return objects_list, round(diff_time, 4)

def detail(request, post_id):
    review = Review_Models.objects.get(id=post_id)

    img_url = review.imgfile.url

    # 이미지 분류 함수 호출(이미지는 url형태로 넘겨주기)
    cnn_result, cnn_diff_time = img_domain_clf(img_url)
    yolo_result, yolo_diff_time = img_object_clf(img_url)

    # print(f"수정 전: {review.domain_clf}")

    # 결과를 받아와서 필드 값 수정 및 저장
    review.domain_clf = cnn_result
    review.objects_clf = yolo_result
    review.save()


    # print(f"수정 후: {review.domain_clf}")


    return render(request, 'Reviews/review_detail.html', {'review':review})