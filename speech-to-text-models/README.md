# Speech-to-Text Models (음성-텍스트 변환 모델)

이 저장소는 다양한 음성-텍스트 변환(Speech-to-Text, STT) 모델을 비교하기 위한 프레임워크를 제공합니다. 특히 OpenAI의 Whisper와 Facebook의 Wav2Vec2 모델을 중점적으로 비교합니다. 한국어와 영어 언어 변환을 모두 지원하며 Docker 컨테이너 환경에서 실행되도록 설계되었습니다.

## 📋 프로젝트 구조

```
speech-to-text-models/
├── .project_root          # 프로젝트 루트 식별용 마커 파일
├── data/                  # 입력 파일용 데이터 디렉토리
├── models/                # 다운로드/캐시된 모델 디렉토리
├── runs/                  # 변환 결과 출력 디렉토리
├── src/
│   ├── utils/
│   │   └── pathfinder.py  # 프로젝트 경로 처리 유틸리티
│   └── whisper/           # STT 모델 구현
│       ├── whisper_trans.py      # Whisper 모델 구현
│       ├── wavvec.py             # Wav2Vec2 모델 구현
│       └── test.py               # pathfinder 테스트 스크립트
├── docker-compose.yml     # Docker Compose 설정
├── Dockerfile.dev         # 개발 환경 Dockerfile
└── Dockerfile             # 프로덕션 환경 Dockerfile
```

## 🚀 기능

- 자동 루트 디렉토리 감지 기능을 갖춘 유연한 프로젝트 구조
- 다양한 STT 모델 지원:
  - OpenAI Whisper (turbo 모델)
  - Facebook Wav2Vec2 (한국어: wav2vec2-large-xlsr-korean, 영어: wav2vec2-base-960h)
- 비디오 파일에서 오디오 추출
- 타임스탬프가 있는 변환 출력
- 일관된 환경을 위한 Docker 기반 배포

## ⚙️ 설정 및 설치

### 사전 요구사항

- Docker 및 Docker Compose
- FFmpeg (Docker 환경에 포함됨)

### 시작하기

1. 이 저장소를 복제합니다:
   ```bash
   git clone https://github.com/yourusername/speech-to-text-models.git
   cd speech-to-text-models
   ```

2. 프로젝트 루트 디렉토리에 `.project_root` 파일을 생성합니다:
   ```bash
   touch .project_root
   ```

3. 개발 환경 시작:
   ```bash
   docker compose up --build dev
   ```

4. 프로덕션 환경용:
   ```bash
   docker compose up --build prod
   ```

## 💻 사용법

### Whisper 모델 실행하기

```bash
docker exec -it speech-to-text-models-dev-1 zsh
cd src/whisper
python whisper_trans.py
```

### Wav2Vec2 모델 실행하기

```bash
docker exec -it speech-to-text-models-dev-1 zsh
cd src/whisper
python wavvec.py
```

### 입력 사용자 정의

오디오 또는 비디오 파일을 `data` 디렉토리에 넣고 각 스크립트의 파일 경로를 업데이트하세요.

예를 들어, `whisper_trans.py` 또는 `wavvec.py`에서 다음과 같이 수정하세요:

```python
# 이 줄을 입력 파일을 가리키도록 변경하세요
video_path = get_project_path('data/your_audio_or_video_file.mp4')
```

## 📊 성능 분석

성능 분석 결과:

1. **정확도**:
   - Whisper는 일반적으로 한국어와 영어 변환 모두에서 Wav2Vec2보다 우수한 성능을 보임
   - Whisper는 더 나은 문맥 이해와 자연스러운 문장 구성을 보여줌

2. **모델 특성**:
   - **Whisper**:
     - turbo 모델(1.5GB)도 좋은 성능을 보여줌
     - large 모델은 더 나은 결과를 제공할 가능성이 높음
   
   - **Wav2Vec2**:
     - 기본 모델은 상용화에 적합하지 않은 성능을 보여줌
     - 한국어 모델은 large 모델을 사용함에도 추가 fine-tuning이 필요함
     - 영어 base 모델은 기대 이하의 성능을 보여줌

## 🔍 구현 세부사항

### 경로 찾기 유틸리티

이 프로젝트는 프로젝트 루트를 찾고 프로젝트 어디서나 파일을 참조할 수 있는 유연한 유틸리티를 포함합니다:

```python
from src.utils.pathfinder import find_project_root, get_project_path

# 프로젝트 루트 찾기
root = find_project_root()

# 특정 파일 또는 디렉토리 경로 가져오기
config_path = get_project_path('config/settings.yaml')
```

### 오디오 추출

이 시스템은 FFmpeg를 사용하여 비디오 파일에서 오디오를 추출할 수 있습니다:

```python
# wavvec.py의 예시
extract_audio_from_video(video_path, audio_path)
```

## 🧪 향후 개선 사항

- 더 많은 STT 모델 지원 추가 (예: Mozilla DeepSpeech)
- 여러 파일의 일괄 처리 구현
- 더 쉬운 비교를 위한 웹 인터페이스 추가
- 더 많은 언어 지원
- 특정 도메인에 대한 fine-tuning 옵션
- 실시간 변환 성능 측정

## 📝 참고 사항

- 프로젝트 초기에는 오타로 인해 디렉토리 이름을 'wisper'로 사용했으나, 현재는 정확한 이름인 'whisper'로 수정함
- 상용 환경에서는 우수한 성능으로 인해 Whisper가 권장됨
- Wav2Vec2는 fine-tuning 후 특정 사용 사례에 적합할 수 있음

## 🔗 의존성

- Python 3.11
- PyTorch
- Transformers (Hugging Face)
- Whisper
- soundfile
- FFmpeg
- Docker