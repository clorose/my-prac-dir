# 기계 가공 데이터 분석 프로젝트

이 프로젝트는 기계 가공 프로세스의 데이터를 수집, 분석하고 제품 품질을 예측하는 머신러닝 모델을 개발하는 것을 목표로 합니다.

## 요구사항

이 프로젝트를 실행하기 위해 다음 라이브러리가 필요합니다:

- fastapi==0.115.0
- matplotlib==3.9.2
- numpy==2.1.1
- pandas==2.2.2
- scikit_learn==1.5.2
- seaborn==0.13.2
- uvicorn==0.30.6
- xgboost==2.1.1

## 설치 방법

1. 이 저장소를 클론합니다:
   ```
   git clone [저장소 URL]
   ```

2. 프로젝트 디렉토리로 이동합니다:
   ```
   cd [프로젝트 디렉토리 이름]
   ```

3. 필요한 라이브러리를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 실행 방법

프로젝트의 메인 함수를 실행하여 데이터 분석 및 모델 학습을 시작할 수 있습니다:

```
python main.py
```

메인 함수는 데이터 로딩, 전처리, 모델 학습, 결과 시각화 등의 전체 프로세스를 순차적으로 실행합니다. 상세한 로그와 결과는 콘솔에 출력됩니다.

## 프로젝트 구조

```
C:\_YHJ\fast\backend\ml\
│
├── output\
│   ├── processed_data_XGModel_120915.csv
│   ├── processed_data_RFModel_121114.csv
│   ├── processed_data_RFModel_120758.csv
│   └── __init__.py
│
├── data\
│   ├── Machine_Tool_Data.csv
│   └── __init__.py
│
├── models\
│   ├── __pycache__\
│   ├── xg_model.py
│   ├── rf_model.py
│   ├── knn_model.py
│   └── __init__.py
│
├── utils\
│   ├── __pycache__\
│   ├── visualization.py
│   └── __init__.py
│
├── preprocessing\
│   ├── __pycache__\
│   ├── data_preprocessing.py
│   └── __init__.py
│
├── main.py
├── config.json
└── __init__.py
```

## 데이터 설명

프로젝트에서 사용되는 CSV 파일(Machine_Tool_Data.csv)은 다음과 같은 필드를 포함합니다:

1. Timestamp: 데이터 기록 시간
2. Machine_ID: 기계 식별자
3. Material_Type: 가공 중인 재료 유형
4. Cutting_Speed: 절삭 속도 (m/min)
5. Feed_Rate: 이송 속도 (mm/rev)
6. Depth_of_Cut: 절삭 깊이 (mm)
7. Tool_Usage_Time: 공구 사용 시간 (분)
8. Vibration: 진동 수준 (mm/s^2)
9. Coolant_Temperature: 냉각제 온도 (°C)
10. Power_Consumption: 전력 소비량 (kW)
11. Cycle_Time: 가공 사이클 시간 (초)
12. Operator_ID: 작업자 식별자
13. Batch_Number: 생산 배치 번호
14. Product_ID: 제품 식별자
15. Tool_ID: 사용 중인 공구 식별자
16. Spindle_Speed: 스핀들 속도 (RPM)
17. Spindle_Load: 스핀들 부하 (%)
18. Feed_Load: 이송 부하 (%)
19. Axis_Position_X: X축 위치 (mm)
20. Axis_Position_Y: Y축 위치 (mm)
21. Axis_Position_Z: Z축 위치 (mm)
22. Surface_Roughness: 표면 거칠기 측정값 (μm)
23. Surface_Roughness_Status: In-spec / Out-of-spec
24. Dimensional_Accuracy: 치수 정확도 측정값 (mm)
25. Dimensional_Accuracy_Status: In-spec / Out-of-spec
26. Defect_Type: None / Scratch / Dent / Misalignment 등
27. Final_Inspection_Result: Pass / Fail

이 데이터셋은 가공 과정에서 실시간으로 수집되는 데이터(1-21)와 품질 검사 과정에서 얻어지는 데이터(22-27)를 모두 포함합니다.

## 데이터 사용 방법

1. 1-21번 필드는 가공 과정의 특성(feature)으로 사용됩니다.
2. 22-26번 필드는 중간 품질 지표로, 특성이나 추가적인 목표 변수로 활용될 수 있습니다.
3. Final_Inspection_Result(27번)는 주요 목표 변수(target variable)로 사용됩니다.
4. 모델은 1-26번 필드의 데이터를 바탕으로 Final_Inspection_Result를 예측하도록 학습됩니다.


# 기계 가공 데이터 CSV 구조

| 열 이름               | 데이터 유형 | 설명                                  | 예시 값              |
|-----------------------|-------------|---------------------------------------|----------------------|
| Timestamp             | Datetime    | 데이터 기록 시간                      | 2024-09-26 10:30:15  |
| Machine_ID            | String      | 기계 식별자                           | M001, M002           |
| Material_Type         | String      | 가공 중인 재료 유형                   | Steel, Aluminum      |
| Cutting_Speed         | Float       | 절삭 속도 (m/min)                     | 150.5, 200.3         |
| Feed_Rate             | Float       | 이송 속도 (mm/rev)                    | 0.2, 0.3             |
| Depth_of_Cut          | Float       | 절삭 깊이 (mm)                        | 1.5, 2.0             |
| Tool_Usage_Time       | Integer     | 공구 사용 시간 (min)                  | 120, 180             |
| Vibration             | Float       | 진동 수준 (mm/s²)                     | 2.5, 3.8             |
| Coolant_Temperature   | Float       | 냉각제 온도 (°C)                      | 25.5, 28.3           |
| Power_Consumption     | Float       | 전력 소비량 (kW)                      | 5.2, 6.8             |
| Cycle_Time            | Integer     | 가공 사이클 시간 (s)                  | 300, 450             |
| Operator_ID           | String      | 작업자 식별자                         | OP001, OP002         |
| Batch_Number          | String      | 생산 배치 번호                        | B001, B002           |
| Product_ID            | String      | 제품 식별자                           | P001, P002           |
| Tool_ID               | String      | 공구 식별자                           | T001, T002           |
| Spindle_Speed         | Integer     | 스핀들 속도 (RPM)                     | 1000, 1500           |
| Spindle_Load          | Float       | 스핀들 부하 (%)                       | 75.5, 82.3           |
| Feed_Load             | Float       | 이송 부하 (%)                         | 60.2, 70.8           |
| Axis_Position_X       | Float       | X축 위치 (mm)                         | 100.5, 150.3         |
| Axis_Position_Y       | Float       | Y축 위치 (mm)                         | 50.2, 75.8           |
| Axis_Position_Z       | Float       | Z축 위치 (mm)                         | 25.5, 30.2           |
| Surface_Roughness     | Float       | 표면 거칠기 측정값 (μm)               | 2.5, 3.2             |
| Dimensional_Accuracy  | Float       | 치수 정확도 측정값 (mm)               | 0.03, 0.06           |
| Defect_Type           | String      | 결함 유형 (있는 경우)                 | None, Scratch, Dent  |
| Quality_Result        | Integer     | 최종 검사 결과 (0=불합격, 1=합격)     | 0, 1                 |

참고: 
1. 'Quality_Result' 열은 예측을 위한 목표 변수로, 0은 검사 불합격(불량품)을 나타내고 1은 검사 합격(양품)을 나타냅니다.
2. 단위는 실제 산업 현장에서 일반적으로 사용되는 것을 반영했습니다. 

## 결과 해석

실행 후 생성되는 처리된 데이터와 모델 출력 결과는 `output` 폴더에 저장됩니다. 

이러한 결과를 바탕으로 다음과 같은 분석이 가능합니다:
1. 어떤 가공 파라미터가 제품 품질에 가장 큰 영향을 미치는지 파악
2. 불량품 발생을 최소화하기 위한 최적의 가공 조건 도출
3. 품질 검사 과정 개선을 위한 인사이트 도출
4. 예측 모델을 통한 실시간 품질 모니터링 시스템 구축 가능성 평가

이를 통해 생산 프로세스 개선, 품질 향상, 비용 절감 등의 전략을 수립할 수 있습니다.