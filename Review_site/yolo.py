from ultralytics import YOLO

import time
import math

import tensorflow as tf
from tensorflow.keras.preprocessing import image

FILE_PATH = "C:/Users/DaonWoori/OptimizedOfficeAI/Review_site/media/review_images/notebook.png"

def calculate_distance(point):
    x_centroid , y_centroid = 0.5, 0.5
    return math.sqrt((x_centroid - point[0])**2 + (y_centroid - point[1])**2)

# 이미지 도메인 분류 로직
def img_domain_clf(img_url=""):
    # 이미지 경로 설정(받아온 url과 로컬 환경의 경로 합쳐주기)
    path = FILE_PATH

    # 이미지 불러오기
    img = image.load_img(path, target_size=(224, 224))

    # 이미지 전처리
    img = image.img_to_array(img)
    img = img / 255.0
    img = tf.expand_dims(img, axis=0)

    # AI 모델 로드
    model = tf.keras.models.load_model('C:/Users/DaonWoori/OptimizedOfficeAI/Review_site//ai_models/CNN_Model_Dataset2.h5', compile=False)
    
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

    print(domain)

    return domain, round(diff_time, 4)

# 이미지 클래스 분류 로직
def img_object_clf(img_url):
    # 모델 불러오기 
    model = YOLO("C:/Users/DaonWoori/OptimizedOfficeAI/Review_site/ai_models/best.pt")
    names = model.names

    print(names)

    # 62f9a36ea3cea.jpg
    # calculator186_gjB6pWv.jpg
    # 이미지 분류 수행
    start_time = time.time()
    result = model.predict(source=FILE_PATH)
    # 이미지 분류 수행")e
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

    print(object_clf)

    # return objects_list[distances.index(min(distances))], round(diff_time, 4)

img_object_clf(None)
img_domain_clf()