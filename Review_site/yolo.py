from ultralytics import YOLO

import time
import math

def calculate_distance(point):
    x_centroid , y_centroid = 0.5, 0.5
    return math.sqrt((x_centroid - point[0])**2 + (y_centroid - point[1])**2)

# 이미지 클래스 분류 로직
def img_object_clf(img_url):
    # 모델 불러오기 
    model = YOLO("C:/Users/DaonWoori/OptimizedOfficeAI/Review_site/ai_models/best.pt")
    names = model.names

    # 이미지 분류 수행
    start_time = time.time()
    result = model.predict(source="C:/Users/DaonWoori/OptimizedOfficeAI/Review_site/media/review_images/calculator186_gjB6pWv.jpg")
    end_time = time.time()

    diff_time = end_time - start_time

    #오브젝트별 중심 거리 
    distances = []

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
            print(names[int(box.cls)])
        print(distances)

    objects_list = []

    return objects_list, round(diff_time, 4)

img_object_clf(None)