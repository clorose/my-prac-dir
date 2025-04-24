# 에어컨 OPC UA 제어 시스템

중앙제어형 에어컨 컨셉으로 OPC UA 테스트를 위해 만든 프로젝트.
온도, 습도, 전력 사용량, 전기 요금, 누진 요금 등을 시뮬레이션하고 GUI를 통해 제어 및 모니터링 기능을 제공함.

## 🔧 구성 요소

- `server.py`: 에어컨 시뮬레이션 서버
- `client.py`: PyQt5 기반 GUI 클라이언트
- `simpleServer.py`: 최소 구현 OPC UA 서버 (예제용)
- `simpleClient.py`: 최소 GUI 클라이언트 (예제용)

## ✅ 주요 기능

### 🖥️ 서버 (`server.py`)
- 에어컨 상태 변수 정의:
  - **Power** (bool, writable): 전원 On/Off
  - **TargetTemperature** (float, writable): 목표 온도
  - **CurrentTemperature**: 현재 온도
  - **Humidity**: 습도
  - **PowerUsage**: 전력 사용량
  - **ElectricityCost**: 전기 요금
  - **CurrentRate**: 현재 적용 요금
  - **OperationTime**: 가동 시간
- **냉방 시뮬레이션**: 목표 온도 대비 현재 온도 차에 따라 냉방 속도 조절
- **습도 시뮬레이션**: 상대 습도에 따라 제습 속도 조절
- **전력 사용량 계산**: 기본 소비전력 + 온도 차 + 고온 보정 + 습도 보정
- **누진 요금 계산**: 사용량에 따라 세 단계 단가 적용
  - 200kWh 이하: 93.3원/kWh
  - 200~400kWh: 187.9원/kWh
  - 400kWh 초과: 280.6원/kWh
- **커스텀 이벤트 전송**: 상태 변화 시 이벤트 발생 (온도, 전원 상태 포함)

### 🖱️ 클라이언트 (`client.py`)
- PyQt5 + asyncio 통합 GUI
- 서버와 OPC UA 연결 후 주요 변수 구독:
  - **CurrentTemperature**, **Humidity**, **PowerUsage**, **ElectricityCost**, **Power**
- GUI 요소:
  - 온도/습도 프로그레스 바
  - 전력 사용량, 요금 표시
  - 목표 온도 설정 버튼
  - 전원 ON/OFF 토글

## 📦 요구 사항

- Python 3.13 이상
- Poetry (의존성 관리)

### 의존성
- `asyncua`: OPC UA 통신
- `PyQt5`: GUI
- `qasync`: Qt + asyncio 연동
- `python-dotenv`: 환경변수 로딩
- `black`: 코드 포매터 (개발용)

## 🚀 설치 및 실행

### 1. 저장소 복제
```bash
git clone <repository-url>
cd opcua
```

### 2. 의존성 설치
```bash
poetry install
```

### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일 생성:
```bash
cp .env.example .env
```

필요에 따라 `.env` 파일 편집:
```
SERVER_HOST=192.0.0.1  # 자신의 IP 주소로 변경
SERVER_PORT=4840
```

### 4. 실행

#### 서버 실행
```bash
poetry run python opcua/server.py
```

#### 클라이언트 실행
```bash
poetry run python opcua/client.py
```

#### 예제용 간단 버전
```bash
# 간단한 서버 실행
poetry run python opcua/simpleServer.py
# 간단한 클라이언트 실행
poetry run python opcua/simpleClient.py
```

## 📂 프로젝트 구조
```
opcua/
├── pyproject.toml      # Poetry 설정
├── poetry.lock         # 고정된 의존성
├── .env.example        # 환경 변수 예제 파일
└── opcua/
    ├── server.py           # 메인 에어컨 서버
    ├── client.py           # 메인 GUI 클라이언트
    ├── simpleServer.py     # 단순화된 예제 서버
    └── simpleClient.py     # 단순화된 예제 클라이언트
```

## ⚙️ 작동 방식

1. 서버는 `AirConditioner` 객체 아래 주요 노드들을 생성
2. 클라이언트는 `.env`로 설정된 주소로 서버 연결
3. 주요 변수들을 구독하고 값 변경 시 GUI 업데이트
4. 사용자가 목표 온도나 전원 설정을 조작하면 서버에 반영
5. 서버는 상태를 시뮬레이션하고 이벤트와 요금 등을 갱신

## 🧠 참고

* 누진 요금 로직은 `server.py` 내부 `calculate_progressive_rate()` 함수에 구현
* 클라이언트는 `client.py`에서 구독 기반 실시간 업데이트 수행
* 서버는 냉방/제습 상황을 1초 주기로 반영하며, OPC UA 이벤트도 전송함