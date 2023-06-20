from django.shortcuts import render, redirect, HttpResponse
from .forms import FileUploadForm
from .models import FileUpload

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import time

# Create your views here.

# 입력받는 페이지 로직
def fileUpload(request):
    ### 사용자가 폼을 통해 입력을 했을 경우, 
    if request.method == 'POST':

        img = request.FILES["imgfile"]

        new_file = FileUpload(
            imgfile = img
        )

        # 입력받은 데이터를 데이터베이스에 저장 -> 자동으로 id 생성
        new_file.save()

        # 결과보기 페이지에 id 값 같이 넘겨주기 -> url(fileupload/results/<id>)
        return redirect('result', post_id=new_file.id)
    
    ### 사용자가 입력하기 전, 폼을 화면에 출력해주는 것
    else:
        fileuploadForm = FileUploadForm()
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

# 이미지 분류 로직
def img_clf(img_url):
    # 이미지 경로 설정(받아온 url과 로컬 환경의 경로 합쳐주기)
    path = "C:/Users/DaonWoori/programming/dev_django/image_pro" + img_url

    # 이미지 불러오기
    img = image.load_img(path, target_size=(224, 224))

    # 이미지 전처리
    img = image.img_to_array(img)
    img = img / 255.0
    img = tf.expand_dims(img, axis=0)

    # AI 모델 로드
    model = tf.keras.models.load_model('C:/Users/DaonWoori/programming/dev_django/image_pro/model/model_16.h5')
    
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

# 결과보기 페이지 관련 로직
def result(request, post_id):
    # 넘겨받은 아이디를 사용해서 해당 데이터 불러오기
    file = FileUpload.objects.get(id=post_id)
    # 이미지 주소 불러오기
    img_url = file.imgfile.url

    # 이미지 분류 함수 호출(이미지는 url형태로 넘겨주기)
    result, diff_time = img_clf(img_url)

    return render(request, 'image_views.html', {'file':img_url, 'result':result, 'time':diff_time})

