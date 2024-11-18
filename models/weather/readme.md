# Weather Prediction Service

기상청 API를 활용한 기상 예측 서비스입니다. LSTM 모델을 사용하여 기온과 습도를 예측합니다.

## 프로젝트 구조
```
weather/
├── app/                      # 메인 애플리케이션 코드
│   ├── api/                  # API 관련 코드
│   │   ├── routes.py        # API 엔드포인트 정의
│   │   └── schemas.py       # 데이터 검증 스키마
│   ├── core/                # 핵심 설정
│   │   ├── config.py        # 설정 관리
│   │   ├── exceptions.py    # 예외 클래스
│   │   ├── logging.py       # 로깅 설정
│   │   └── dependencies.py  # FastAPI 의존성
│   ├── models/              # ML 모델 클래스
│   │   └── predictor.py     # 예측 모델 클래스
│   ├── services/            # 비즈니스 로직
│   │   ├── data_collector.py    # 데이터 수집
│   │   ├── model_trainer.py     # 모델 학습
│   │   └── predictor.py         # 예측 서비스
│   └── utils/               # 유틸리티 함수
│       ├── weather_api.py   # 날씨 API 관련
│       └── date_utils.py    # 날짜 처리 유틸리티
├── data/                    # 데이터 저장소
│   └── climate_model/       # 학습된 모델과 관련 파일
├── tests/                   # 테스트 코드
├── .env                     # 환경 변수
├── .gitignore              # Git 제외 파일
├── .project_root           # 프로젝트 루트 표시
├── config.py               # 설정 파일
├── main.py                 # 애플리케이션 시작점
└── requirements.txt        # 의존성 목록
```

## 필요 사항
- Python 3.8+
- FastAPI
- Uvicorn
- TensorFlow
- pandas
- numpy
- scikit-learn
- python-dotenv

## 설치

1. 저장소 클론
```bash
git clone https://github.com/yourusername/weather.git
cd weather
```

2. 가상환경 생성 및 활성화

Linux/Mac:
```bash
python -m venv .venv
# 가상 환경 활성화
source .venv/bin/activate
```

Windows:
```bash
python -m venv .venv
# 가상 환경 활성화
.venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
touch .env
```
`.env` 파일에 아래 내용 추가
```bash
WEATHER_API_KEY=your_api_key_here
```

5. 프로젝트 루트 표시 파일 생성
```bash
touch .project_root
```

6. 가상환경 종료
```bash
deactivate
```

## 실행
```bash
python3 app.py
```

- API 서버: `http://localhost:8000`
- API 문서: `http://localhost:8000/docs`
- 대체 문서: `http://localhost:8000/redoc`

## API 엔드포인트

### 예측
```http
GET /api/v1/predict
```
향후 12개월의 기상 예측 결과를 반환합니다.

### 학습
```http
POST /api/v1/train
```
새로운 데이터로 모델을 재학습합니다.

### 상태 확인
```http
GET /api/v1/status
```
현재 모델의 상태와 마지막 학습 일자를 확인합니다.

## 기능
- 기상청 API를 통한 과거 기상 데이터 수집
- LSTM 모델을 사용한 기온/습도 예측
- FastAPI를 통한 RESTful API 제공
- 자동 모델 학습 및 업데이트
- 비동기 처리를 통한 효율적인 데이터 수집

## 개발 가이드

### 코드 스타일
- PEP 8 준수
- Type Hints 사용
- Docstring 필수 작성

### 테스트
```bash
pytest tests/
```

### 린트 검사
```bash
pylint app/ tests/
```

## 라이선스
MIT License