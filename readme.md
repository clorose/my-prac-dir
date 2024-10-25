```bash
weather/
├── app/                      # 메인 애플리케이션 코드
│   ├── api/                  # API 관련 코드
│   │   ├── __init__.py      # Python 패키지 선언
│   │   ├── routes.py        # API 엔드포인트 정의
│   │   └── schemas.py       # 데이터 검증 스키마
│   ├── core/                # 핵심 설정
│   │   ├── __init__.py
│   │   ├── config.py        # 설정 관리
│   │   └── logging.py       # 로깅 설정
│   ├── models/              # ML 모델 클래스
│   │   ├── __init__.py
│   │   └── predictor.py     # 예측 모델 클래스
│   ├── services/            # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── data_collector.py    # 데이터 수집
│   │   ├── model_trainer.py     # 모델 학습
│   │   └── predictor.py         # 예측 서비스
│   └── utils/               # 유틸리티 함수
│       ├── __init__.py
│       └── weather_api.py   # 날씨 API 관련
├── data/                    # 데이터 저장소
│   └── climate_model/       # 학습된 모델과 관련 파일
│       ├── model.keras      # 저장된 Keras 모델
│       ├── scaler.pkl       # 데이터 스케일러
│       ├── last_sequence.npy    # 마지막 시퀀스
│       └── last_date.txt    # 마지막 날짜
├── tests/                   # 테스트 코드
├── .env                     # 환경 변수
└── main.py                  # 애플리케이션 시작점
```
