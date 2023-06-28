from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, reverse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from Reviews.models import Review_Models, UserProfile
from .forms import FileUploadForm, RegistrationForm, LoginForm, DeleteAccountForm


# 로그인 및 회원가입에 관한 모듈들 
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



import tensorflow as tf
from tensorflow.keras.preprocessing import image

from ultralytics import YOLO

import time
import math

file = "/Users/bchank/Review_site" 

def calculate_distance(point):
    x_centroid , y_centroid = 0.5, 0.5
    return math.sqrt((x_centroid - point[0])**2 + (y_centroid - point[1])**2)

# 이미지 도메인 분류 로직
def img_domain_clf(img_url):
    # 이미지 경로 설정(받아온 url과 로컬 환경의 경로 합쳐주기)
    global file
    path = file + img_url
    print(path)

    # 이미지 불러오기
    img = image.load_img(path, target_size=(224, 224))

    # 이미지 전처리
    img = image.img_to_array(img)
    img = img / 255.0
    img = tf.expand_dims(img, axis=0)

    # AI 모델 로드
    model = tf.keras.models.load_model('/Users/bchank/Review_site/ai_models/CNN_Model_Dataset2.h5', compile=False)
    
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
    global file
    path = file + img_url

    # 모델 불러오기 
    model = YOLO("/Users/bchank/Review_site/ai_models/best.pt")
    names = model.names

    # 62f9a36ea3cea.jpg
    # calculator186_gjB6pWv.jpg
    # 이미지 분류 수행
    start_time = time.time()
    result = model.predict(source=path)
    end_time = time.time()

    diff_time = end_time - start_time

    #오브젝트별 중심 거리 
    distances = []
    objects_list = []

    # result 내의 결과값들
    for r in result:
        for box in r.boxes:
            x1 = float(box.xyxyn[0][0])
            y1 = float(box.xyxyn[0][1])
            x2 = float(box.xyxyn[0][2])
            y2 = float(box.xyxyn[0][3])

            x_mid , y_mid = ( x1 + x2 ) / 2 , ( y1 + y2 ) / 2
            mid = [x_mid, y_mid]
            distance = calculate_distance(mid)
            distances.append(distance)

            # class id 에 해당하는 이름 출력하기
            objects_list.append(names[int(box.cls)])

    try:
        object_clf = objects_list[distances.index(min(distances))]
    except:
        object_clf = "None"

    return object_clf, round(diff_time, 4)

# 리뷰 조회 페이지 로직
def index(request):
    #### 정렬 기능 
    # sort라는 이름으로 들어온 값 가져오기(값이 없다면 None)
    sort = request.GET.get('sort', None)

    # 날짜와 관련한 정렬
    if sort == 'date-new':
        reviews = Review_Models.objects.all().order_by('-dt_created')
    elif sort== 'date-old':
        reviews = Review_Models.objects.all().order_by('dt_created')
    # 별점과 관련한 정렬
    elif sort == 'likes-high':
        reviews = Review_Models.objects.all().order_by('-ratings')
    elif sort == 'likes-low':
        reviews = Review_Models.objects.order_by('ratings')
    # 정렬 없을 떄
    else:
        reviews = Review_Models.objects.all().order_by('-dt_created') # 데이터 전체 불러오기

    # paginator 객체 생성(queryset, 한 페이지에서 보여줄 포스트 개수)
    paginator = Paginator(reviews, 9)
    page = request.GET.get('page', None) # page라는 명으로 들러온 값을 가져오겠다(ex) ~/?page=4
    page_obj = paginator.get_page(page) # 페이지가 숫자가 아닌 경우 첫 페이지를 반환, 음수나 범위를 벗어난 경우 마지막 페이지 반환 -> Page 객체 반환

    # return render(request, 'Reviews/index.html', {'reviews':reviews})
    return render(request, 'Reviews/index.html', {'page_obj':page_obj, 'paginator':paginator, 'sort':sort})

# 리뷰 작성 페이지 로직
@csrf_exempt
def upload(request):
    ### 사용자가 폼을 통해 입력을 했을 경우, 
    if request.method == 'POST':

        # 입력된 내용들을 form이라는 변수에 저장
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid(): # form이 유효하다면,
            post = form.save(commit=False) # form 데이터 저장(임시 저장)
            post.save() # form 데이터를 DB에 저장

            ### 데이터 분류 로직 ###
            review = Review_Models.objects.get(id=post.id)

            # 이미지 분류 함수 호출(이미지는 url형태로 넘겨주기)
            cnn_result, cnn_diff_time = img_domain_clf(review.imgfile.url)
            yolo_result, yolo_diff_time = img_object_clf(review.imgfile.url)

             # 결과를 받아와서 필드 값 수정 및 저장
            review.domain_clf = cnn_result
            review.objects_clf = yolo_result
            review.save()

            # 결과보기 페이지에 id 값 같이 넘겨주기
            return redirect('detail', post_id=post.id)
        
    ### 사용자가 입력하기 전, 새로운 폼을 생성
    else:
        form = FileUploadForm()

    # form이 유효하지 않다면, 기존 form 형식 유지 
    return render(request, 'Reviews/review_upload.html', {'form':form})

# 리뷰 상세보기 페이지 로직
def detail(request, post_id):
    review = Review_Models.objects.get(id=post_id)

    return render(request, 'Reviews/review_detail.html', {'review':review})

# 리뷰 수정페이지 로직
@csrf_exempt
def update(request, post_id):
    review = Review_Models.objects.get(id=post_id)

    ### 사용자가 폼을 통해 입력을 했을 경우, 
    if request.method == 'POST':
        # 입력된 내용들을 form이라는 변수에 저장
        update_form = FileUploadForm(request.POST, request.FILES, instance=review)

        if update_form.is_valid(): # form이 유효하다면,
            post = update_form.save(commit=False) # form 데이터 저장(임시 저장)
            post.save() # form 데이터를 DB에 저장

            ### 데이터 분류 로직 ###
            review = Review_Models.objects.get(id=post.id)

            # 이미지 분류 함수 호출(이미지는 url형태로 넘겨주기)
            cnn_result, cnn_diff_time = img_domain_clf(review.imgfile.url)
            yolo_result, yolo_diff_time = img_object_clf(review.imgfile.url)

             # 결과를 받아와서 필드 값 수정 및 저장
            review.domain_clf = cnn_result
            review.objects_clf = yolo_result
            review.save()

            # 결과보기 페이지에 id 값 같이 넘겨주기
            return redirect('detail', post_id=post.id)
    else:
        # 기존에 입력받은 데이터를 그대로 출력 g
        update_form = FileUploadForm(instance=review)

    return render(request, 'Reviews/review_upload.html', {'form':update_form, 'review':review})

# 리뷰 삭제 페이지
@csrf_exempt
def delete(request, post_id):
    review = Review_Models.objects.get(id=post_id)
    review.delete()

    return redirect('index')

# 로그인 관련 함수 정의
@csrf_exempt
def login_view(request):

    # Base_with_nav_html에 있는 상단 로그인 버튼을 클릭하는 경우, 즉 요청이 Post가 아닌 경우 
    # Login 관련 html로 렌더링
    if request.method =='GET':
        form = LoginForm()
        return render(request, 'Reviews/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # 이메일과 비밀번호를 사용하여 인증을 수행
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # 인증에 성공한 경우, 로그인 처리
                login(request, user)
                return redirect('index')  # 로그인 후 이동할 페이지로 변경
            else:
                message = '유효하지 않은 이메일 또는 비밀번호입니다.'
                return render(request, 'Reviews/login.html', {'form': form, 'message': message})
        else:
            return render(request, 'Reviews/login.html', {'form': form})

# 회원 가입에 관한 함수 정의
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                message = '비밀번호가 일치하지 않습니다.'
                return render(request, 'Reviews/register.html', {'form': form, 'message': message})

            if password == confirm_password:
                try:
                    User.objects.get(email=email)
                    message = '이미 사용 중인 이메일입니다.'
                    return render(request, 'Reviews/register.html', {'form': form, 'message': message})
                except User.DoesNotExist:
                    user = User(
                        email=email,
                        username=email,
                        password=make_password(password)
                    )
                    user.save()
                    message = '회원가입이 완료되었습니다.'
                    return render(request, 'Reviews/register.html', {'form': form, 'message': message})
        
    elif request.method == 'GET':
        form = RegistrationForm()
    
    return render(request, 'Reviews/register.html', {'form': form})

# 회원 탈퇴에 관한 함수 정의
@csrf_exempt
@login_required
def deleteaccount(request):
    # form = DeleteAccountForm()

    if request.method == 'POST':
        user = request.user
        password = request.POST['password']

        # 비밀번호 확인 절차
        if user.check_password(password):
            # 사용자 계정을 삭제한 후 로그아웃 처리
            user.delete()
            logout(request)
            message = '회원 탈퇴가 완료되었습니다.'
            return render(request, 'Reviews/deleteaccount.html', {'message':message})
        
        else:   
            message = '비밀 번호가 올바르지 않습니다.'
            return render(request, 'Reviews/deleteaccount.html', {'message':message})
                  
    if request.method == 'GET':
        return render(request, 'Reviews/deleteaccount.html')

@csrf_exempt
def logout_view(request):
    logout(request)  # 로그아웃 실행
    return redirect('index') 

# 내가 본 리뷰 기능 구현을 위한 함수 정의
@csrf_exempt
def viewed_reviews(request):
    user_profile = UserProfile.objects.get(user=request.user)
    viewed_reviews = user_profile.viewed_reviews.all()
    context = {'viewed_reviews': viewed_reviews}
    return render(request, 'viewed_reviews.html', context)
