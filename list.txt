# 내 레포지토리 목록 및 후기

## 레포지토리 목록

- [x] Fast → fastapi-factory-ml
- [x] lstm-java → WeatherForecastLSTM
- [x] mnist → CNN-HandwrittenDigitRec 
- [x] opcua → opcua-ac-simulator
- [x] weather
- [x] whisper → speech-to-text-models
- [x] yolo

## 레포지토리 설명 및 후기

### Fast → fastapi-factory-ml
간단한 머신러닝 불량예측 프로그램. 이 프로젝트를 진행할 당시에는 가상환경(venv)도 사용하지 않았음. 이름이 'Fast'인 이유는 Fast 프로토콜로 통신했기 때문. 프로젝트 용도와 사용 기술을 명확히 표현하기 위해 이름을 변경함.

### lstm-java → WeatherForecastLSTM
LSTM을 통한 시계열 예측 프로그램. 기상청 API를 사용했고, 코틀린 미들웨어를 통해 프론트엔드와 통신함. 프로젝트 용도와 기술을 명확히 표현하기 위해 이름을 변경함.

### mnist → CNN-HandwrittenDigitRec
MNIST(Modified National Institute of Standards and Technology database)를 활용한 손글씨 인식 머신러닝 프로젝트. 프로젝트 용도와 사용 기술을 명확히 표현하기 위해 이름 변경함.

### opcua → opcua-ac-simulator
OPC UA 통신 연습용 프로젝트. 이 프로젝트로 인해 레포지토리 이름을 'ml-practice-repo'에서 'my-prac-dir'로 변경하게 됨. Poetry를 처음 사용해본 프로젝트. 프로젝트의 목적을 더 명확히 표현하기 위해 이름을 변경함.

### weather
날씨 예측 프로젝트. 이 코드가 나중에 lstm-java(WeatherForecastLSTM) 프로젝트에 통합됨.

### whisper → speech-to-text-models
음성 인식 프로젝트. MP4 파일을 사용하여 음성을 텍스트로 변환함. OpenAI의 Whisper 모델이 Facebook의 wav2vec2 모델보다 뛰어난 인식률을 보임. wav2vec2는 WAV 파일이 아닌 MP4를 사용해서 인식률이 낮았을 수도 있음. 프로젝트의 목적과 내용을 더 명확히 표현하기 위해 이름을 변경함.

### Yolo8
YOLO(You Only Look Once) 모델을 활용한 이미지 인식 프로젝트. 이 프로젝트에서 처음으로 Docker를 사용함. Poetry가 PyTorch와 호환이 잘 되지 않아 여러 시도 끝에 Docker로 전환했더니 문제가 해결됨. Python 3.12와 YOLO11을 사용해볼걸 하는 아쉬움이 남음.

## 기술 스택 발전 과정
- 초기: 기본 Python 환경 (가상환경 없이)
- 중기: Poetry 도입
- 후기: Docker 활용

## 향후 계획
- 레포지토리 이름을 더 명확하고 일관성 있게 정리 (완료)
- 각 프로젝트의 README 보완
- 최신 기술 스택 적용 고려 (Python 3.12, 최신 모델 등)