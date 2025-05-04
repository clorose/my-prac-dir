# YOLO 객체 탐지 프로젝트

Docker와 Poetry를 활용한 YOLOv8 기반 객체 탐지 시스템.
컴퓨터 비전 분석을 위한 Python 환경을 쉽게 구축하고 YOLO 모델을 실행할 수 있는 설정을 제공합니다.

## 🔧 구성 요소

- `Dockerfile`: 프로덕션용 컨테이너 설정
- `Dockerfile.dev`: 개발용 컨테이너 설정
- `docker-compose.yml`: 서비스 구성 설정
- `main.py`: YOLO 모델 실행 스크립트
- `test.py`: 환경 테스트 스크립트

## ✅ 주요 기능

### 🐳 Docker 환경
- **다중 플랫폼 지원**: linux/amd64, linux/arm64 (Apple Silicon 포함)
- **볼륨 마운트**: 데이터, 모델, 소스코드, 결과 디렉토리 자동 연결
- **Poetry 캐시**: 의존성 설치 속도 최적화

### 🐍 개발 환경
- **Python 3.11** 기반
- **Poetry** 의존성 관리
- **자동화된 가상환경** 설정

### 🔍 객체 탐지
- **YOLOv8** 모델 활용
- **GPU 가속화** (CUDA 지원 시)
- **이미지/비디오 처리**
- **결과 시각화 및 저장**

## 📦 요구 사항

- Docker 및 Docker Compose
- 또는 Python 3.11 및 Poetry (로컬 개발 시)

### 의존성
- `ultralytics`: YOLOv8 구현체
- `torch`/`torchvision`: PyTorch 프레임워크
- `opencv-python-headless`: 이미지 처리
- `pandas`/`seaborn`: 데이터 분석 및 시각화
- `tensorboard`: 모델 훈련 모니터링
- `tqdm`: 진행 상황 표시
- `python-dotenv`: 환경변수 관리

## 🚀 설치 및 실행

### 방법 1: Docker 컨테이너 (권장)

#### 개발 환경 실행
```bash
docker compose up dev
```

#### 컨테이너 접속
```bash
docker exec -it yolo-dev-1 bash
```

#### 테스트 실행
```bash
python src/test.py
```

#### 객체 탐지 실행
```bash
python src/main.py
```

### 방법 2: 로컬 개발 환경

#### 1. Pyenv 및 Poetry 설치
```bash
pipx install pyenv
pipx install poetry
```

#### 2. Python 3.11 설치
```bash
pyenv install 3.11
pyenv local 3.11

# 설정 확인
python --version  # 결과: Python 3.11.x
```

#### 3. 가상환경 설정
```bash
poetry env use python3.11
poetry install
```

## 📂 프로젝트 구조
```
yolo/
├── data/              # 데이터셋 저장 디렉토리
├── models/            # 모델 가중치 파일(.pt) 저장
├── runs/              # 모델 실행 결과 저장
├── src/               # 소스 코드
│   ├── main.py        # 메인 실행 파일
│   ├── hello.py       # 간단한 테스트 스크립트
│   └── test.py        # 환경 테스트 스크립트
├── Dockerfile         # 프로덕션용 Docker 설정
├── Dockerfile.dev     # 개발용 Docker 설정
├── docker-compose.yml # Docker 컨테이너 구성
├── pyproject.toml     # Poetry 의존성 정의
└── README.md          # 프로젝트 문서
```

## ⚙️ 작동 방식

1. Docker 또는 Poetry로 환경 설정
2. 필요한 YOLO 모델 가중치를 `/models` 디렉토리에 배치
3. 분석할 이미지를 `/data` 디렉토리에 배치
4. `main.py` 실행 (경로 수정 필요)
5. 결과는 `/runs` 디렉토리에 저장됨

## 🧠 커스텀 모델/이미지 사용
`src/main.py` 파일을 수정하여 다른 모델이나 이미지 경로 지정:
```python
from ultralytics import YOLO

# 모델 로드 (경로 수정)
model = YOLO('models/yolov8m.pt')

# 이미지로 객체 탐지 (경로 수정)
results = model('data/images')

# 결과 저장
results = model('data/images', save=True)
```

## 🚁 프로덕션 환경

경량화된 Docker 이미지 제공:
```bash
docker compose up prod
```

## 📋 의존성 관리

```bash
# 패키지 추가
poetry add 패키지명

# 개발용 패키지 추가
poetry add --group dev 패키지명
```