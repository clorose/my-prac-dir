from ultralytics import YOLO

# 모델 로드
model = YOLO('../model/yolov8m.pt')

# 이미지로 객체 탐지
results = model('../images')

# 결과 출력 (리스트의 각 요소에 접근)
for result in results:
    print(result.boxes.data)  # 바운딩 박스, 클래스, 신뢰도 점수 출력
    # 또는
    print(result.boxes.cls)   # 클래스만 출력
    # 또는
    print(result.boxes.conf)  # 신뢰도 점수만 출력


results = model('../images', save=True)