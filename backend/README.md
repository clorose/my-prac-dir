# FastAPI 금속 제조 품질 예측

이 프로젝트는 FastAPI를 사용하여 금속 제조 품질 예측 모델을 위한 API를 생성합니다. 다양한 제조 매개변수를 기반으로 제품 품질을 분석하고 예측하기 위한 데이터 시각화 및 기계 학습 구성 요소를 포함합니다.

## 주요 기능

- 효율적인 API 개발을 위한 FastAPI 백엔드
- pandas, matplotlib, seaborn을 사용한 데이터 분석 및 시각화
- scikit-learn 및 XGBoost를 사용한 기계 학습 모델
- 실시간 예측 엔드포인트

## 사전 요구 사항

- Python 3.8+
- pip (Python 패키지 관리자)

## 설치 방법

1. 저장소 클론:
   ```
   git clone https://github.com/yourusername/fastapi-metal-manufacturing.git
   cd fastapi-metal-manufacturing
   ```

2. 가상 환경 생성 (선택사항이지만 권장):
   ```
   python -m venv venv
   source venv/bin/activate  # Windows에서는 `venv\Scripts\activate` 사용
   ```

3. 필요한 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

## 사용 방법

FastAPI 서버 실행:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API는 `http://localhost:8000`에서 사용할 수 있습니다.

## API 문서

서버가 실행되면 자동 대화형 API 문서에 접근할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 프로젝트 구조

```
fastapi-metal-manufacturing/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── prediction_model.py
│   └── routers/
│       └── api.py
│
├── data/
│   └── Metal_Manufacturing_Dataset.csv
│
├── requirements.txt
└── README.md
```