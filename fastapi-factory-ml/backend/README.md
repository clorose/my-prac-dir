# 📊 ML-Factory: 기계 공정 데이터 분석 플랫폼

AI 모델 기반 분석을 제공하는 FastAPI + React 풀스택 프로젝트입니다.  
사용자는 CSV 파일을 업로드하고, 머신러닝 모델을 통해 분석 결과를 시각화하여 확인할 수 있습니다.

## 🛠 주요 기술 스택

| 영역            | 기술                                                              |
| :-------------- | :---------------------------------------------------------------- |
| 백엔드 (서버)   | Python 3.x, FastAPI, Uvicorn, Pydantic Settings                   |
| ML 프레임워크   | scikit-learn, XGBoost, pandas, NumPy, joblib, Matplotlib, seaborn |
| 프론트엔드 (UI) | React 18, TypeScript, Vite, Styled-Components                     |
| 데이터 시각화   | Matplotlib, seaborn, 3D 시각화                                    |
| 기타            | Axios (HTTP 통신), Material-UI (테이블 컴포넌트), CORS 지원       |

## 📂 프로젝트 구조

```plaintext
ml-factory/
├── backend/                # FastAPI 서버
│   ├── app/                # 서버 애플리케이션
│   │   ├── core/           # 설정 관리
│   │   ├── middleware/     # 미들웨어 (로깅 등)
│   │   ├── routes/         # API 라우트
│   │   └── service/        # 서비스 레이어
│   ├── ml/                 # 머신러닝 모듈
│   │   ├── common/         # 공통 ML 기능
│   │   │   ├── data_processing.py       # 데이터 분할 및 전처리
│   │   │   ├── feature_importance.py    # 특성 중요도 계산
│   │   │   ├── file_operations.py       # 모델 저장/로드 및 CSV 파일 처리
│   │   │   └── model_evaluation.py      # 모델 성능 평가
│   │   ├── models/         # ML 모델 구현
│   │   │   ├── knn/        # K-Nearest Neighbors 모델
│   │   │   ├── rf/         # Random Forest 모델
│   │   │   └── xgb/        # XGBoost 모델
│   │   ├── preprocessing/  # 데이터 전처리
│   │   ├── utils/          # 유틸리티 기능
│   │   └── trained_models/ # 학습된 모델 저장소 (.joblib)
│   └── uploads/            # 업로드된 파일 저장소
├── frontend/               # React 클라이언트
│   ├── public/             # 정적 리소스
│   └── src/
│       ├── assets/         # 이미지
│       ├── components/     # UI 컴포넌트
│       │   ├── FileUpload/
│       │   ├── RecentUploads/
│       │   └── ui/         # 공통 UI 컴포넌트
│       ├── pages/          # 페이지 컴포넌트
│       │   ├── mainPage/
│       │   └── testPage/   # 분석 결과 페이지
│       ├── styles/         # 공통 스타일
│       └── types/          # 타입 정의
└── README.md               # 프로젝트 설명서
```

## 🚀 실행 방법

### 1. 환경 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 설정합니다:

```
PROJECT_NAME="FastAPI Project"
VERSION="0.1.0"
HOST="0.0.0.0"
PORT=8000
ALLOWED_ORIGINS=["http://localhost:5173"]
UPLOAD_DIR="uploads"
ML_OUTPUT_DIR="{your_path}/fast/backend/ml/trained_models"
```

환경에 맞게 경로를 수정하세요.

### 2. Backend 실행 (FastAPI 서버)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> 기본 포트: **localhost:8000**

API 엔드포인트:
- `/`: 홈 엔드포인트
- `/upload`: CSV 파일 업로드 및 분석 요청
- `/api/files`: 저장된 모델 파일 목록 조회
- `/api/predict`: 선택된 모델로 예측 수행
- `/static`: 분석 결과 정적 파일 제공

### 3. Frontend 실행 (React 앱)

```bash
cd frontend
npm install  # 또는 pnpm install
npm run dev  # 또는 pnpm dev
```

> 기본 포트: **localhost:5173**

## 🧩 주요 기능

| 기능              | 설명                                                   | 구현 상태 |
| :---------------- | :----------------------------------------------------- | :-------- |
| CSV 파일 업로드   | 프론트에서 CSV 파일 업로드 후 서버에 제출              | ✅ 완료    |
| 모델 선택         | 여러 머신러닝 모델 중 선택하여 분석                    | ✅ 완료    |
| 데이터 전처리     | 다양한 전처리 방법 지원 (결측치, 정규화, 이상치 처리)  | ✅ 완료    |
| 모델 학습 및 평가 | 다양한 평가 지표로 모델 성능 분석 (정확도, F1, AUC)    | ✅ 완료    |
| 특성 중요도 분석  | 모델의 특성 중요도 계산 및 시각화                      | ✅ 완료    |
| 결과 시각화       | 3D 산점도, 상관관계 히트맵, 박스 플롯 등 다양한 시각화 | ✅ 완료    |
| 예측 수행         | 학습된 모델을 사용하여 새 데이터 예측                  | ✅ 완료    |
| 합성 데이터 생성  | 테스트용 기계 공정 데이터 생성 기능                    | ✅ 완료    |

## 🔧 백엔드 개발자를 위한 안내

### API 엔드포인트 구현

새로운 API 엔드포인트를 추가하려면 `app/routes/api.py` 파일을 수정하세요:

```python
@router.get("/api/your-endpoint")
async def your_endpoint():
    return {"message": "Your endpoint works!"}
```

### 머신러닝 모델 개발

현재 지원되는 모델은 다음과 같습니다:
- XGBoost (`XGModel`): 그래디언트 부스팅 기반 분류 모델
- K-Nearest Neighbors (`KNNModel`): 거리 기반 분류 모델
- Random Forest (`RFModel`): 앙상블 의사결정 트리 모델

새로운 머신러닝 모델을 추가하려면:

1. `ml/models/` 디렉토리에 새 모듈 생성
2. 기존 모델 클래스의 인터페이스를 따라 구현:
   - `load_data_and_train_model()`: 데이터 로드 및 모델 학습
   - `predict()`: 예측 수행
   - `get_model_performance()`: 모델 성능 평가
   - `save_model()` / `load_model()`: 모델 저장 및 로드

3. `config.json`에 새 모델 설정 추가

### 데이터 전처리 확장

`ml/preprocessing/data_preprocessing.py`에 새로운 전처리 방법을 추가할 수 있습니다:

- 결측치 처리: `handle_missing_values()`
- 이상치 제거: `remove_outliers()`
- 스케일링: `normalize_data()`
- 특성 엔지니어링: `feature_engineering()`

### 설정 변경

`app/core/config.py`에서 애플리케이션 설정을 수정할 수 있습니다.

## 🎨 프론트엔드 개발자를 위한 안내

### 컴포넌트 추가

새로운 UI 컴포넌트는 `frontend/src/components/` 디렉토리에 추가하세요.

### API 호출

백엔드 API 호출은 Axios를 사용하여 수행합니다:

```typescript
import axios from 'axios';

const SERVER_URL = import.meta.env.VITE_SERVER_URL || 'http://localhost:8000';

// API 호출 예제
const fetchData = async () => {
  const response = await axios.get(`${SERVER_URL}/api/endpoint`);
  return response.data;
};
```

### 시각화 컴포넌트 추가

분석 결과를 표시하는 새로운 시각화 컴포넌트를 추가하려면:

1. `frontend/src/components/visualizations/` 디렉토리 생성
2. 데이터 타입에 맞는 컴포넌트 구현 (차트, 그래프 등)
3. 백엔드에서 받은 데이터를 시각화 컴포넌트에 연결

## 📊 데이터 시각화 기능

백엔드에서 제공하는 시각화 기능:

- 3D 산점도: 상위 중요 특성 3개를 3D 공간에 시각화
- 상관관계 히트맵: 특성 간의 상관관계 시각화
- 특성 중요도 플롯: 모델이 판단한 특성 중요도 시각화
- 박스 플롯: 클래스별 특성 분포 시각화
- 산점도 행렬: 특성 간의 관계를 다차원적으로 시각화

## 🔍 테스트 데이터 생성

테스트를 위한 합성 데이터는 `ml/data_gen.py`를 사용하여 생성할 수 있습니다:

```bash
cd backend/ml
python data_gen.py
```

이 스크립트는 기계 공정 데이터를 시뮬레이션하여 CSV 파일로 생성합니다.

## 🛠️ 향후 계획 및 개선 사항

- [ ] 하이퍼파라미터 최적화: 그리드/랜덤 서치 기능 추가
- [ ] 딥러닝 모델 통합: TensorFlow/PyTorch 모델 지원
- [ ] 교차 검증: K-폴드 교차 검증 구현
- [ ] 실시간 모니터링: 스트리밍 데이터 지원
- [ ] 모델 버전 관리: 모델 성능 추적 및 버전 관리
- [ ] API 문서화: Swagger/ReDoc 통합