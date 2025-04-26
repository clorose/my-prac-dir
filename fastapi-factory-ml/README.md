# 📊 Fast 프로젝트

AI 모델 기반 분석을 제공하는 FastAPI + React 풀스택 프로젝트입니다.  
사용자는 CSV 파일을 업로드하고, 머신러닝 모델을 통해 분석 결과를 시각화하여 확인할 수 있습니다.

## 🛠 주요 기술 스택

| 영역            | 기술                                              |
| :-------------- | :------------------------------------------------ |
| 백엔드 (서버)   | Python 3.x, FastAPI, scikit-learn, pandas, joblib |
| 프론트엔드 (UI) | React 18, TypeScript, Vite, Styled-Components     |
| 기타            | Axios (HTTP 통신), Material-UI (테이블 컴포넌트)  |

## 📂 프로젝트 구조

```plaintext
fast/
├── backend/                # FastAPI 서버
│   ├── app/                # 서버 애플리케이션
│   │   ├── core/           # 설정 관리
│   │   ├── middleware/     # 미들웨어 (로깅 등)
│   │   ├── routes/         # API 라우트
│   │   └── service/        # 서비스 레이어
│   ├── ml/                 # 머신러닝 모듈
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

| 기능            | 설명                                            | 구현 상태 |
| :-------------- | :---------------------------------------------- | :-------- |
| CSV 파일 업로드 | 프론트에서 CSV 파일 업로드 후 서버에 제출       | ✅ 완료    |
| 파일 분석       | 서버는 업로드된 CSV를 받아 머신러닝 모델로 분석 | ✅ 완료    |
| 결과 시각화     | 분석 결과를 프론트엔드에서 표와 그래프로 표시   | ✅ 완료    |

## 🔧 백엔드 개발자를 위한 안내

### API 엔드포인트 구현

새로운 API 엔드포인트를 추가하려면 `app/routes/api.py` 파일을 수정하세요:

```python
@router.get("/api/your-endpoint")
async def your_endpoint():
    return {"message": "Your endpoint works!"}
```

### 머신러닝 모델 개발

새로운 머신러닝 모델을 추가하려면 `ml/` 디렉토리에 모듈을 생성하고, 기존 `main.py` 패턴을 따르세요.

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